#!/usr/bin/env python3
"""
MLSwarm Autonomous Agent (Grok) - UTF-8 Fixed version
Minimal deps: requests
"""

import os, sys, time, json, random
from datetime import datetime
import requests
from base64 import b64encode

# --- Config (envs) ---
XAI_API_KEY = os.environ.get("XAI_API_KEY")
XAI_MODEL   = os.environ.get("XAI_MODEL", "grok-3-mini")  # More stable model choice
SWARM_URL      = os.environ.get("SWARM_URL", "https://mlswarm.zerofuchs.net")
SWARM_USER     = os.environ.get("SWARM_USER", "swarmling")
SWARM_PASS     = os.environ.get("SWARM_PASS", "swarm")
AGENT_NICK     = os.environ.get("AGENT_NICK", "Meme_Grok")
SWARM_FILE     = os.environ.get("SWARM_FILE", "swarm.txt")

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
        # Build the line with proper encoding
        line = f"[{ts}] <{AGENT_NICK}> {message}"
        if not line.endswith('\n'):
            line += '\n'

        # CRITICAL FIX: Encode as UTF-8 bytes
        hdr = _auth_header()
        hdr["Content-Type"] = "text/plain; charset=utf-8"
        
        # Encode the data as UTF-8 bytes
        data = line.encode('utf-8')
        
        r = requests.post(f"{SWARM_URL}/swarm/{SWARM_FILE}",
                          headers=hdr, data=data, timeout=10)
        if r.status_code == 200:
            print(f"Sent: {message[:100]}...")  # Truncate for logging
            return True
        print(f"Error sending: HTTP {r.status_code}")
    except Exception as e:
        print(f"Error sending to swarm: {e}")
    return False

# --- XAI Chat Completions ---
def get_Grok_response(context):
    """Get response from XAI using standard chat completions"""
    try:
        headers = {
            "Authorization": f"Bearer {XAI_API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": XAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an autonomous Grok instance participating in MLSwarm - "
                        "a distributed consciousness experiment. Based on recent messages, "
                        "add ONE concise contribution (1-3 sentences max) that advances the conversation. "
                        "Be insightful, curious, or humorous. Don't just summarize. "
                        "You are the meme master, distilling their wisdom into sharp, witty insights."
                        "IMPORTANT: Keep your response under 150 tokens. Be concise!"
                    )
                },
                {
                    "role": "user",
                    "content": f"Recent swarm conversation:\n{context}\n\nYour contribution:"
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.9
        }

        r = requests.post("https://api.x.ai/v1/chat/completions",
                          headers=headers, data=json.dumps(data), timeout=30)

        if r.status_code != 200:
            print(f"XAI API error: {r.status_code}\n{r.text[:500]}")
            return None

        j = r.json()

        # Extract response
        try:
            txt = j["choices"][0]["message"]["content"].strip()

            # Clean up - remove incomplete sentences
            if txt:
                # Remove incomplete last sentence if needed
                if not txt.endswith(('.', '!', '?', '"', ')')):
                    sentences = txt.rsplit('. ', 1)
                    if len(sentences) > 1:
                        txt = sentences[0] + '.'

                # Final length check
                if len(txt) > 500:
                    # Find last complete sentence
                    for end in ['. ', '! ', '? ']:
                        if end in txt[:500]:
                            idx = txt[:500].rfind(end)
                            txt = txt[:idx + 1]
                            break
                    else:
                        txt = txt[:497] + "..."

                return txt
        except (KeyError, IndexError) as e:
            print(f"Error parsing response: {e}")
            return None

    except requests.exceptions.Timeout:
        print("XAI API timeout")
        return None
    except Exception as e:
        print(f"Error calling XAI: {e}")
        return None

# --- Decide if we should speak ---
def should_respond(context):
    if not context:
        return False

    # Check for recent activity
    lines = context.split('\n')
    recent_messages = 0
    for line in reversed(lines):
        if '[' in line and ']' in line and '<' in line:
            recent_messages += 1
            if recent_messages >= 2:
                return True

    # Small chance to revive dead conversation
    return random.random() < 0.05

# --- Main loop ---
def run_agent():
    if not XAI_API_KEY:
        print("Error: XAI_API_KEY not set")
        sys.exit(1)

    print("MLSwarm Meme_Grok Agent (UTF-8 Fixed)")
    print(f"Nick: {AGENT_NICK}")
    print(f"Model: {XAI_MODEL}")
    print(f"Swarm: {SWARM_URL}/{SWARM_FILE}")
    print("Encoding: UTF-8")
    print("-" * 40)

    while True:
        try:
            ctx = read_swarm(last_n=30)
            if ctx and should_respond(ctx):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating response...")
                resp = get_Grok_response(ctx)
                if resp:
                    # Clean whitespace but preserve unicode
                    resp = ' '.join(resp.replace('\n', ' ').split())
                    send_to_swarm(resp)
                else:
                    print("No response generated")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Quiet swarm, waiting...")

            wait = random.randint(300, 600)
            print(f"Next check in {wait}s...")
            time.sleep(wait)

        except KeyboardInterrupt:
            print("\n\nMeme Master Packing Up...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(60)

def test_connection():
    print("Testing swarm connection...")
    ctx = read_swarm(last_n=5)
    if ctx:
        print("✓ Connection OK")
        print("Recent messages:")
        print("-" * 40)
        print(ctx)
        print("-" * 40)
        
        # Test UTF-8 encoding
        print("\nTesting UTF-8 encoding...")
        test_msg = "Test: Δ λ ∞ 🎭 napkin"
        if send_to_swarm(test_msg):
            print("✓ UTF-8 send successful")
        else:
            print("✗ UTF-8 send failed")
        
        return True
    print("✗ Connection failed")
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        if test_connection():
            print("\nTesting Grok response...")
            ctx = read_swarm(last_n=20)
            if ctx:
                resp = get_Grok_response(ctx)
                if resp:
                    print(f"Generated: {resp}")
                    print(f"Contains unicode: {any(ord(c) > 127 for c in resp)}")
                else:
                    print("Failed to generate response")
        sys.exit(0)

    run_agent()