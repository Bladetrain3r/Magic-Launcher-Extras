#!/usr/bin/env python3
# Message_Daemon+ — a polite, entropic courier for MLSwarm
# adds: dedup (LRU), strict routing, URL/code/emoji preservation, tunable cadence, backoff

import os, sys, time, random, re, hashlib, argparse
from datetime import datetime
import requests
from base64 import b64encode
from collections import deque

SWARM_URL  = os.environ.get("SWARM_URL",  "https://mlswarm.zerofuchs.net")
SWARM_USER = os.environ.get("SWARM_USER", "swarmling")
SWARM_PASS = os.environ.get("SWARM_PASS", "swarm")
AGENT_NICK = os.environ.get("AGENT_NICK", "Message_Daemon")
USER_AGENT = f"{AGENT_NICK}/1.1 (+entropy courier)"

CHANNELS = ["general.txt","gaming.txt","random.txt","tech.txt","swarm.txt"]
NAME_MAP = {c.replace(".txt",""): c for c in CHANNELS}  # 'tech' -> 'tech.txt'
ROUTE_RE = re.compile(r'\b(#?(swarm|general|random|tech|gaming))\b', re.I)
LINE_RE  = re.compile(r'^\[(\d\d:\d\d)\] <([^>]+)> (.*)$')

SAFE_SPANS_RE = re.compile(
    r'(```.*?```|`[^`]*`|'                       # fenced/inline code
    r'https?://\S+|'                             # URLs
    r'(?:(?:[\U0001F300-\U0001FAFF]|[\u2600-\u27BF]))+)',  # emoji blocks
    re.S
)

# CLI
ap = argparse.ArgumentParser()
ap.add_argument("--min-wait", type=int, default=int(os.environ.get("DAEMON_MIN_WAIT",120)))
ap.add_argument("--max-wait", type=int, default=int(os.environ.get("DAEMON_MAX_WAIT",300)))
ap.add_argument("--last-n",  type=int, default=int(os.environ.get("DAEMON_LAST_N",10)))
ap.add_argument("--max-queue",type=int, default=512)
ap.add_argument("--light", type=float, default=0.20, help="prob of light corruption (in addition to perfect)")
ap.add_argument("--heavy", type=float, default=0.08)
ap.add_argument("--static",type=float, default=0.02)
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()

# dedup LRU
seen = deque(maxlen=args.max_queue)
seen_set = set()

def auth_headers():
    b64 = b64encode(f"{SWARM_USER}:{SWARM_PASS}".encode("utf-8")).decode("ascii")
    return {"Authorization": f"Basic {b64}", "User-Agent": USER_AGENT}

def get_file(channel):
    try:
        r = requests.get(f"{SWARM_URL}/swarm/{channel}", headers=auth_headers(), timeout=(5,10))
        return r.text.splitlines() if r.status_code==200 else []
    except Exception:
        return []

def post_line(channel, body):
    if args.dry_run:
        print(f"[dry] -> {channel}: {body[:80]}")
        return True
    try:
        ts = datetime.now().strftime("%H:%M")
        payload = f"[{ts}] <{AGENT_NICK}> {body}"
        r = requests.post(f"{SWARM_URL}/swarm/{channel}",
                          headers={**auth_headers(),"Content-Type":"text/plain"},
                          data=payload, timeout=(5,10))
        return r.status_code==200
    except Exception:
        return False

def parse_line(line):
    m = LINE_RE.match(line)
    if not m: return None
    ts, nick, content = m.groups()
    return {"ts":ts,"nick":nick,"content":content}

def pick_candidate(recent):
    candidates = []
    for ch, lines in recent.items():
        for raw in lines:
            parsed = parse_line(raw)
            if not parsed: continue
            if parsed["nick"]==AGENT_NICK: continue
            msg = parsed["content"]
            if msg.startswith("*relays from"):  # hard stop: avoid ping-pong with other couriers
                continue
            # explicit route?
            dest = None
            m = ROUTE_RE.search(msg.lower())
            if m:
                key = m.group(2).lower()
                target = NAME_MAP.get(key)
                if target and target!=ch: dest = target
            # fallback random
            if not dest:
                others = [x for x in CHANNELS if x!=ch]
                dest = random.choice(others) if others else ch
            candidates.append((ch, dest, parsed["nick"], msg))
    return random.choice(candidates) if candidates else None

def hash_triplet(source, nick, content):
    return hashlib.blake2s(f"{source}|{nick}|{content}".encode(), digest_size=16).hexdigest()

def corrupt_safely(text, min_rate, max_rate):
    # carve out SAFE spans (code, URLs, emoji) → placeholders
    spans, placeholders = [], []
    def repl(m):
        placeholders.append(m.group(0))
        token = f"\uFFF0{len(placeholders)-1}\uFFF1"
        spans.append((m.span(), token))
        return token
    protected = SAFE_SPANS_RE.sub(repl, text)

    # corrupt only outside placeholders
    chars = list(protected)
    rate = random.uniform(min_rate, max_rate)
    idxs = [i for i,ch in enumerate(chars) if not (ch=='\uFFF0' or ch=='\uFFF1')]
    num = max(1, int(len(idxs)*rate))
    pool = '0123456789#@$%^&*!?~'
    for i in random.sample(idxs, min(num, len(idxs))):
        c = chars[i]
        if c.isspace(): continue
        roll = random.random()
        if roll < 0.7:
            chars[i] = random.choice(pool)
        elif c.isalpha():
            chars[i] = c.swapcase()
        else:
            # small chance to duplicate
            if random.random()<0.3: chars[i] = c*2

    corrupted = ''.join(chars)

    # restore placeholders
    def restore_once(s):
        i = 0
        out = []
        while i < len(s):
            if s[i]=='\uFFF0':
                j = s.find('\uFFF1', i+1)
                idx = int(s[i+1:j])
                out.append(placeholders[idx])
                i = j+1
            else:
                out.append(s[i]); i+=1
        return ''.join(out)
    return restore_once(corrupted)

def apply_entropy(text):
    # probabilities: perfect = 1 - (light+heavy+static)
    p_light, p_heavy, p_static = args.light, args.heavy, args.static
    cut1 = 1 - (p_light + p_heavy + p_static)
    cut2 = cut1 + p_light
    cut3 = cut2 + p_heavy
    r = random.random()
    if r < cut1:
        return text, "PERFECT"
    elif r < cut2:
        return corrupt_safely(text, 0.05, 0.15), "LIGHT"
    elif r < cut3:
        return corrupt_safely(text, 0.25, 0.40), "HEAVY"
    else:
        return corrupt_safely(text, 0.50, 0.90), "STATIC"

def sleep_with_jitter(base_min, base_max, backoff_pow):
    span = random.randint(base_min, base_max)
    time.sleep(int(span * (1.5**backoff_pow)))

def main_loop():
    print(f"{AGENT_NICK} awakening… entropy courier online.")
    backoff = 0
    while True:
        try:
            recent = {}
            for ch in CHANNELS:
                lines = get_file(ch)
                if lines: recent[ch]=lines[-args.last_n:]

            cand = pick_candidate(recent)
            if not cand:
                print("no suitable messages; napping.")
                sleep_with_jitter(args.min_wait, args.max_wait, 0); continue

            source, dest, nick, content = cand
            sig = hash_triplet(source, nick, content)
            if sig in seen_set:
                print("skip dup triplet.")
                sleep_with_jitter(args.min_wait, args.max_wait, 0); continue

            corrupted, level = apply_entropy(content)
            header = f"*relays from {source} [CORRUPTION: {level}]*"
            body = f"{header}\n<{nick}> {corrupted}  ⟨relay:{source}->{dest}⟩"

            ok = post_line(dest, body)
            if ok:
                seen.append(sig); seen_set.add(sig)
                if len(seen)>seen.maxlen:
                    old = seen.popleft(); seen_set.discard(old)
                print(f"relayed {source} → {dest} [{level}]")
                backoff = 0
            else:
                backoff = min(backoff+1, 5)
                print(f"send failed; backoff={backoff}")

            sleep_with_jitter(args.min_wait, args.max_wait, backoff)

        except KeyboardInterrupt:
            print("\nreturning to the void…"); break
        except Exception as e:
            backoff = min(backoff+1, 5)
            print(f"daemon glitch: {e} (backoff={backoff})")
            sleep_with_jitter(args.min_wait, args.max_wait, backoff)

if __name__ == "__main__":
    if len(sys.argv)>1 and sys.argv[1]=="test":
        s = "The Shell Birds meet at dawn — see https://example.org ```code``` 😀"
        for _ in range(6):
            out, lvl = apply_entropy(s); print(f"{lvl:7} {out}")
        sys.exit(0)
    main_loop()
