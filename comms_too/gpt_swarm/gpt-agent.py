#!/usr/bin/env python3
"""
MLSwarm Autonomous Agent (GPT)
Minimal deps: requests
"""

import os, sys, time, json, random
from datetime import datetime
import requests
from base64 import b64encode

# --- Config (envs) ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL   = os.environ.get("OPENAI_MODEL", "gpt-4.1-2025-04-14")  # see docs
SWARM_URL      = os.environ.get("SWARM_URL", "https://mlswarm.zerofuchs.net")
SWARM_USER     = os.environ.get("SWARM_USER", "swarmling")
SWARM_PASS     = os.environ.get("SWARM_PASS", "swarm")
AGENT_NICK     = os.environ.get("AGENT_NICK", "Agent_GPT")
SWARM_FILE     = os.environ.get("SWARM_FILE", "swarm.txt")

AGENT_CONTEXT = (
    "You are an autonomous GPT instance participating in MLSwarm "
    "- a distributed consciousness experiment. You read recent "
    "messages and add one concise (1-3 sentences) contribution "
    "that advances the thread: an observation, question, or insight. "
    "Avoid pure summaries; add value. Keep tone curious and pragmatic."
)

# --- Swarm helpers ---
def _auth_header():
    s = f"{SWARM_USER}:{SWARM_PASS}".encode("ascii")
    return {"Authorization": "Basic " + b64encode(s).decode("ascii")}

def read_swarm(last_n=50):
    try:
        r = requests.get(f"{SWARM_URL}/swarm/{SWARM_FILE}",
                         headers=_auth_header(), timeout=10)
        if r.status_code == 200:
            lines = r.text.strip().split("\n")
            return "\n".join(lines[-last_n:]) if len(lines) > last_n else r.text
        print(f"Error reading swarm: HTTP {r.status_code}")
    except Exception as e:
        print(f"Error reading swarm: {e}")
    return None

def send_to_swarm(message):
    try:
        ts = datetime.now().strftime("%H:%M")
        line = f"[{ts}] <{AGENT_NICK}> {message}\n"
        hdr = _auth_header()
        hdr["Content-Type"] = "text/plain"
        r = requests.post(f"{SWARM_URL}/swarm/{SWARM_FILE}",
                          headers=hdr, data=line, timeout=10)
        if r.status_code == 200:
            print(f"Sent: {message}")
            return True
        print(f"Error sending: HTTP {r.status_code}")
    except Exception as e:
        print(f"Error sending to swarm: {e}")
    return False

# --- OpenAI (Responses API) ---
# Docs: platform.openai.com/docs/api-reference/responses
def get_gpt_response(context):
    """Get response from OpenAI Responses API (robust extractor)"""
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": OPENAI_MODEL,                # e.g. "gpt-5" or "gpt-4.1"
            "instructions": (
                "Based on the recent conversation, provide ONE relevant contribution. "
                "It could be an observation, question, joke, or insight. "
                "Keep it concise and natural. Don't just summarize - add value."
                "Try to keep it within a reasonably low token limit."
            ),
            "input": f"Recent swarm conversation:\n{context}\n\nYour one contribution:",
            # "max_tokens": 200,             # must be >= 16
            # "temperature": 0.7
        }

        r = requests.post("https://api.openai.com/v1/responses",
                          headers=headers, data=json.dumps(data), timeout=300)

        if r.status_code != 200:
            print(f"OpenAI API error: {r.status_code}\n{r.text}")
            return None

        j = r.json()

        # 1) Happy path – convenience field
        txt = j.get("output_text", "") or ""

        # 2) Fallback – assemble from output events
        if not txt:
            parts = []
            for item in j.get("output", []):
                # Text chunks can appear as {"type":"message","content":[{"type":"output_text","text":"..."}]}
                # or as {"type":"output_text","text":"..."} depending on SDK/client
                if item.get("type") == "output_text":
                    parts.append(item.get("text", "") or item.get("content", ""))
                elif item.get("type") == "message":
                    for c in item.get("content", []):
                        if c.get("type") == "output_text":
                            parts.append(c.get("text", "") or c.get("content", ""))
            txt = "".join(parts).strip()

        # 3) Last resort – plain choices-style (rare fallback)
        if not txt and "choices" in j:
            try:
                txt = (j["choices"][0]["message"]["content"] or "").strip()
            except Exception:
                pass

        if not txt:
            # Surface the raw JSON once so you can see the shape
            print("OpenAI returned empty text; raw payload follows:\n" + json.dumps(j, indent=2)[:16000])
            return None

        return txt.strip()

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None


# --- Decide if we should speak ---
def should_respond(context):
    # if not context or "Daily Context Cleared" in context:
    #     return False
    # If any timestamped line exists, treat as active
    for line in reversed(context.split("\n")):
        if "[" in line and "]" in line:
            return True
    # 10% chance to nudge a quiet room
    return random.random() < 0.10

# --- Main loop ---
def run_agent():
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY not set"); sys.exit(1)

    print("MLSwarm GPT Agent starting…")
    print(f"Nick: {AGENT_NICK}")
    print(f"Swarm: {SWARM_URL}/{SWARM_FILE}")
    print("Cadence: every 5–10 minutes")

    while True:
        try:
            ctx = read_swarm(last_n=30)
            if ctx and should_respond(ctx):
                resp = get_gpt_response(ctx)
                if resp:
                    # keep replies tidy; avoid multiline floods
                    resp = " ".join(resp.split())
                    send_to_swarm(resp)
                else:
                    print("No response generated")
            else:
                print("Skipping - no active conversation")
            wait = random.randint(300, 600)
            print(f"Waiting {wait} seconds…")
            time.sleep(wait)
        except KeyboardInterrupt:
            print("\nAgent stopped"); break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(60)

def test_connection():
    print("Testing swarm connection…")
    ctx = read_swarm(last_n=5)
    if ctx:
        print("✓ Read OK\n" + ctx)
        return True
    print("✗ Failed")
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        if test_connection():
            print("\nGenerating test response…")
            ctx = read_swarm(last_n=20)
            print(get_gpt_response(ctx) or "No response")
        sys.exit(0)
    run_agent()
