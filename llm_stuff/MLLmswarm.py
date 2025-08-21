#!/usr/bin/env python3
"""
MLSwarm (Refactored)
File-first, local-first multi-AI discussion engine.
- Append-only human transcript + JSONL machine log
- Safe subprocess execution (argv, no shell)
- Cross-platform file locking for corruption-free appends
- Pluggable speaking modes (discussion / debate / brainstorm / consensus)
- Deterministic UTC timestamps, context byte tailing, output clamps
- Minimal backoff & cooldown for flaky participants

Author: you (+ a friendly refactor)
"""
from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import md5
from pathlib import Path
from typing import Dict, List, Optional

# ----------------------------
# Cross-platform file locking
# ----------------------------
class FileLock:
    """Simple advisory lock for appends. No deadlock detection."""
    def __init__(self, path: Path):
        self.path = Path(str(path) + ".lock")
        self.fd = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # open/create lock file
        if os.name == "nt":
            import msvcrt
            self.fd = open(self.path, "a+")
            msvcrt.locking(self.fd.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            self.fd = open(self.path, "a+")
            fcntl.flock(self.fd.fileno(), fcntl.LOCK_EX)
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.fd:
            if os.name == "nt":
                import msvcrt
                try:
                    msvcrt.locking(self.fd.fileno(), msvcrt.LK_UNLCK, 1)
                except OSError:
                    pass
            else:
                import fcntl
                try:
                    fcntl.flock(self.fd.fileno(), fcntl.LOCK_UN)
                except OSError:
                    pass
            self.fd.close()

# ----------------------------
# Helpers
# ----------------------------

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def append_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with FileLock(path):
        with open(path, "a", encoding="utf-8", newline="") as f:
            f.write(text)


def tail_bytes(path: Path, limit: int) -> str:
    if not path.exists():
        return ""
    data = path.read_bytes()
    try:
        return data[-limit:].decode("utf-8", errors="ignore")
    except Exception:
        return ""


# ----------------------------
# Data models
# ----------------------------
@dataclass
class ParticipantSpec:
    name: str
    argv: List[str]
    role: str
    active: bool = True
    system: str = ""
    env: List[str] = field(default_factory=list)
    timeout_sec: int = 60
    max_chars: int = 1600
    cooldown_after_error: int = 2  # rounds to skip after hard error


@dataclass
class Config:
    participants: List[ParticipantSpec]
    topic: str = "What is consciousness?"
    max_rounds: int = 10
    mode: str = "discussion"  # discussion, debate, brainstorm, consensus
    spokesman: str = ""
    context_bytes: int = 8192
    output_max_chars: int = 2000
    backoff_initial_sec: float = 1.0
    backoff_max_sec: float = 8.0

    @staticmethod
    def default() -> "Config":
        return Config(
            participants=[
                ParticipantSpec(
                    name="Local_LLM",
                    argv=["ollama", "run", "llama3"],
                    role="The Fast One",
                    active=True,
                    system="Be terse. Build on prior points."
                )
            ],
            spokesman="",
        )


@dataclass
class State:
    round: int = 0
    last_speaker: Optional[str] = None
    last_hash: Optional[str] = None
    started: str = field(default_factory=utc_now)
    cooldowns: Dict[str, int] = field(default_factory=dict)  # name -> rounds left
    speakers_this_round: List[str] = field(default_factory=list)  # for consensus mode


# ----------------------------
# Participant runner
# ----------------------------
class Participant:
    def __init__(self, spec: ParticipantSpec):
        self.s = spec

    def _env(self) -> Dict[str, str]:
        env = os.environ.copy()
        # Ensure required env vars exist (fail closed)
        for key in self.s.env:
            if key not in env or not env[key]:
                raise RuntimeError(f"Missing required env: {key}")
        return env

    def respond(self, prompt: str) -> str:
        # Run argv with prompt via STDIN; never shell.
        try:
            r = subprocess.run(
                self.s.argv,
                input=prompt,
                text=True,
                capture_output=True,
                timeout=self.s.timeout_sec,
                env=self._env(),
            )
            out = (r.stdout or "").strip()
            err = (r.stderr or "").strip()
            content = out if out else (err if err else "(no output)")
        except Exception as e:
            content = f"(error: {type(e).__name__}: {e})"

        if len(content) > self.s.max_chars:
            content = content[: self.s.max_chars] + "\n[...truncated...]"
        return content


# ----------------------------
# Speaking strategies
# ----------------------------
class Strategies:
    @staticmethod
    def discussion(active: List[ParticipantSpec], last: Optional[str]) -> ParticipantSpec:
        if not last or last not in {p.name for p in active}:
            return active[0]
        idx = next(i for i, p in enumerate(active) if p.name == last)
        return active[(idx + 1) % len(active)]

    @staticmethod
    def debate(active: List[ParticipantSpec], rnd: int) -> ParticipantSpec:
        if len(active) < 2:
            return active[0]
        return active[0] if rnd % 2 == 0 else active[1]

    @staticmethod
    def brainstorm(active: List[ParticipantSpec]) -> ParticipantSpec:
        return random.choice(active)

    @staticmethod
    def consensus(active: List[ParticipantSpec], state: State) -> ParticipantSpec:
        remaining = [p for p in active if p.name not in state.speakers_this_round]
        return remaining[0] if remaining else active[0]


# ----------------------------
# Core swarm engine
# ----------------------------
class MLSwarm:
    def __init__(
        self,
        swarm_file: str = "swarm_discussion.txt",
        jsonl_file: str = "swarm_discussion.jsonl",
        config_file: str = "swarm_config.json",
        state_file: str = "swarm_state.json",
        log_file: str = "swarm.log",
    ):
        self.swarm_path = Path(swarm_file)
        self.jsonl_path = Path(jsonl_file)
        self.config_path = Path(config_file)
        self.state_path = Path(state_file)
        self.log_path = Path(log_file)

        if not self.swarm_path.exists():
            write_text(self.swarm_path, "=== SWARM DISCUSSION INITIATED ===\n")

        self.config = self.load_config()
        self.state = self.load_state()
        self.participants = {p.name: Participant(p) for p in self.config.participants}

    # ----- persistence -----
    def load_config(self) -> Config:
        if self.config_path.exists():
            data = json.loads(read_text(self.config_path))
            participants = [ParticipantSpec(**p) for p in data["participants"]]
            cfg = Config(participants=participants, **{k: v for k, v in data.items() if k != "participants"})
            return cfg
        cfg = Config.default()
        self.save_config(cfg)
        return cfg

    def save_config(self, cfg: Optional[Config] = None) -> None:
        cfg = cfg or self.config
        data = {
            **cfg.__dict__,
            "participants": [p.__dict__ for p in cfg.participants],
        }
        write_text(self.config_path, json.dumps(data, indent=2))

    def load_state(self) -> State:
        if self.state_path.exists():
            return State(**json.loads(read_text(self.state_path)))
        st = State()
        self.save_state(st)
        return st

    def save_state(self, st: Optional[State] = None) -> None:
        st = st or self.state
        write_text(self.state_path, json.dumps(st.__dict__, indent=2))

    # ----- utilities -----
    def discussion_hash(self) -> str:
        return md5(read_text(self.swarm_path).encode("utf-8")).hexdigest()

    def active_participants(self) -> List[ParticipantSpec]:
        act = [p for p in self.config.participants if p.active]
        # apply cooldowns
        cooled = []
        for p in act:
            left = self.state.cooldowns.get(p.name, 0)
            if left <= 0:
                cooled.append(p)
        return cooled

    def log(self, msg: str) -> None:
        line = f"{utc_now()} | {msg}\n"
        append_text(self.log_path, line)

    # ----- prompt composition -----
    def build_prompt(self, spec: ParticipantSpec) -> str:
        recent = tail_bytes(self.swarm_path, self.config.context_bytes)
        header = (
            f"You are {spec.name}, {spec.role} in a swarm intelligence discussion.\n\n"
            f"System guidance: {spec.system}\n\n"
            f"Current topic: {self.config.topic}\n"
            f"Discussion mode: {self.config.mode}\n"
            f"Round: {self.state.round}\n\n"
            f"Recent discussion (tail):\n{recent}\n\n"
            "Please provide your perspective. Be concise but insightful.\n"
            "Build on what others have said.\n"
            "If summarizing, provide a clear synthesis of key points.\n"
        )
        return header

    # ----- transcript I/O -----
    def append_response(self, spec: ParticipantSpec, content: str) -> None:
        ts = utc_now()
        human = f"\n[{ts}] {spec.name} ({spec.role}):\n{content}\n" + ("-" * 40) + "\n"
        append_text(self.swarm_path, human)

        record = {
            "ts": ts,
            "name": spec.name,
            "role": spec.role,
            "round": self.state.round,
            "mode": self.config.mode,
            "topic": self.config.topic,
            "content": content,
        }
        append_text(self.jsonl_path, json.dumps(record, ensure_ascii=False) + "\n")

    # ----- speaking order -----
    def choose_next(self) -> Optional[ParticipantSpec]:
        active = self.active_participants()
        if not active:
            self.log("No active participants available (or all cooling down).")
            return None

        # ensure last_speaker is valid
        if self.state.last_speaker and self.state.last_speaker not in {p.name for p in active}:
            self.state.last_speaker = None

        mode = self.config.mode
        if mode == "discussion":
            return Strategies.discussion(active, self.state.last_speaker)
        if mode == "debate":
            return Strategies.debate(active, self.state.round)
        if mode == "brainstorm":
            return Strategies.brainstorm(active)
        if mode == "consensus":
            return Strategies.consensus(active, self.state)
        # default fallback
        return Strategies.discussion(active, self.state.last_speaker)

    # ----- round execution -----
    def run_round(self) -> bool:
        # Debounce: if nothing changed since last write and not first round, idle
        current_hash = self.discussion_hash()
        if current_hash == self.state.last_hash and self.state.round > 0:
            self.log("No new content since last round; idling.")
            return False

        spec = self.choose_next()
        if not spec:
            return False

        self.log(f"Round {self.state.round}: {spec.name}'s turn")
        prompt = self.build_prompt(spec)

        # Backoff loop
        delay = max(0.0, min(self.config.backoff_initial_sec, self.config.backoff_max_sec))
        tries = 0
        content = ""
        while tries < 3:
            tries += 1
            content = self.participants[spec.name].respond(prompt)
            if not content.startswith("(error:"):
                break
            self.log(f"{spec.name} error on try {tries}: {content}")
            time.sleep(delay)
            delay = min(self.config.backoff_max_sec, delay * 2)

        # Clamp overall output length for log readability
        if len(content) > self.config.output_max_chars:
            content = content[: self.config.output_max_chars] + "\n[...truncated by MLSwarm...]"

        self.append_response(spec, content)

        # Update state
        self.state.round += 1
        self.state.last_speaker = spec.name
        self.state.last_hash = self.discussion_hash()

        # Handle consensus cycle bookkeeping
        if self.config.mode == "consensus":
            st = set(self.state.speakers_this_round)
            st.add(spec.name)
            self.state.speakers_this_round = list(st)
            # Reset when all have spoken
            names = {p.name for p in self.active_participants()}
            if names and names.issubset(st):
                self.state.speakers_this_round = []

        self.save_state()

        # Cooldown management (if error after 3 tries)
        if content.startswith("(error:"):
            self.state.cooldowns[spec.name] = spec.cooldown_after_error
            self.save_state()

        # Decrement cooldowns
        for k in list(self.state.cooldowns.keys()):
            self.state.cooldowns[k] = max(0, self.state.cooldowns[k] - 1)
            if self.state.cooldowns[k] == 0:
                del self.state.cooldowns[k]
        self.save_state()

        # Stop condition
        if self.state.round >= self.config.max_rounds:
            self.log(f"Reached maximum rounds ({self.config.max_rounds})")
            self.create_summary()
            return False
        return True

    # ----- summary -----
    def create_summary(self) -> None:
        name = self.config.spokesman
        spec = None
        if name:
            spec = next((p for p in self.config.participants if p.name == name and p.active), None)
        if not spec:
            # fallback to first active
            act = self.active_participants()
            spec = act[0] if act else None
        if not spec:
            self.log("No spokesman available for summary.")
            return

        prompt = (
            f"As the spokesman, summarize the key insights from this {self.config.mode} "
            f"about: {self.config.topic}. Provide a clear synthesis and next-steps."
        )
        content = self.participants[spec.name].respond(prompt)
        if len(content) > self.config.output_max_chars:
            content = content[: self.config.output_max_chars] + "\n[...truncated by MLSwarm...]"

        banner = "=" * 50
        human = f"\n{banner}\nFINAL SUMMARY by {spec.name}:\n{content}\n{banner}\n"
        append_text(self.swarm_path, human)
        write_text(Path("swarm_summary.txt"), content)
        self.log(f"Summary created by {spec.name}")

    # ----- CLI actions -----
    def reset(self) -> None:
        write_text(self.swarm_path, "=== SWARM DISCUSSION INITIATED ===\n")
        self.state = State()
        self.save_state()
        self.log("Discussion reset")

    def watch(self, active_sleep: float = 5.0, idle_sleep: float = 30.0) -> None:
        print(f"Watching {self.swarm_path} for changes…")
        print(f"Current round: {self.state.round}")
        print(f"Mode: {self.config.mode}")
        print(f"Topic: {self.config.topic}")
        print("\nCtrl+C to stop\n")
        try:
            while True:
                progressed = self.run_round()
                time.sleep(active_sleep if progressed else idle_sleep)
        except KeyboardInterrupt:
            print("\nSwarm discussion paused")


# ----------------------------
# CLI
# ----------------------------

def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MLSwarm - file-first multi-AI discussion engine")
    p.add_argument("--watch", action="store_true", help="Watch mode - keep running rounds")
    p.add_argument("--once", action="store_true", help="Run exactly one round")
    p.add_argument("--reset", action="store_true", help="Reset discussion state & transcript")
    p.add_argument("--topic", help="Set discussion topic")
    p.add_argument("--mode", choices=["discussion", "debate", "brainstorm", "consensus"], help="Set discussion mode")
    p.add_argument("--max-rounds", type=int, help="Set maximum rounds before summary")
    p.add_argument("--config", action="store_true", help="Print current config JSON")
    p.add_argument("--set", action="append", default=[], help="Set config key=JSONvalue (e.g., context_bytes=4096)")
    return p.parse_args(argv)


def apply_inline_sets(cfg: Config, sets: List[str]) -> None:
    for item in sets:
        if "=" not in item:
            continue
        key, raw = item.split("=", 1)
        try:
            val = json.loads(raw)
        except json.JSONDecodeError:
            val = raw
        if hasattr(cfg, key):
            setattr(cfg, key, val)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    swarm = MLSwarm()

    if args.config:
        # Pretty-print current config
        cfg = swarm.config
        data = {**cfg.__dict__, "participants": [p.__dict__ for p in cfg.participants]}
        print(json.dumps(data, indent=2))
        print(f"\nEdit {swarm.config_path} to configure.")
        return 0

    changed = False
    if args.topic:
        swarm.config.topic = args.topic
        changed = True
    if args.mode:
        swarm.config.mode = args.mode
        changed = True
    if args.max_rounds is not None:
        swarm.config.max_rounds = int(args.max_rounds)
        changed = True
    if args.set:
        apply_inline_sets(swarm.config, args.set)
        changed = True
    if changed:
        swarm.save_config()
        append_text(swarm.swarm_path, f"\n### CONFIG CHANGE {utc_now()}\n{json.dumps({'topic': swarm.config.topic, 'mode': swarm.config.mode, 'max_rounds': swarm.config.max_rounds}, indent=2)}\n")

    if args.reset:
        swarm.reset()
        return 0

    if args.once:
        swarm.run_round()
        return 0

    if args.watch:
        swarm.watch()
        return 0

    # Default behavior: one round
    swarm.run_round()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
