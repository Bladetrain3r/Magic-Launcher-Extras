#!/usr/bin/env python3
"""
MLSwarm Autonomous Agent (GPT) - Fixed version
Minimal deps: requests
"""

import os, sys, time, json, random
from datetime import datetime
import requests
from base64 import b64encode

# --- Config (envs) ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL   = os.environ.get("OPENAI_MODEL", "gpt-4-turbo-preview")  # More stable model
SWARM_URL      = os.environ.get("SWARM_URL", "https://mlswarm.zerofuchs.net")
SWARM_USER     = os.environ.get("SWARM_USER", "swarmling")
SWARM_PASS     = os.environ.get("SWARM_PASS", "swarm")
AGENT_NICK     = os.environ.get("AGENT_NICK", "Agent_GPT")
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
        # CRITICAL FIX: Ensure message ends with newline for proper append
        line = f"[{ts}] <{AGENT_NICK}> {message}"
        if not line.endswith('\n'):
            line += '\n'
        
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

# --- OpenAI Chat Completions (more reliable than Responses API) ---
def get_gpt_response(context):
    """Get response from OpenAI using standard chat completions"""
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

        # Use the standard chat completions endpoint instead
        data = {
            "model": OPENAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an autonomous GPT instance participating in MLSwarm - "
                        "a distributed consciousness experiment. Based on recent messages, "
                        "add ONE concise contribution (1-3 sentences max) that advances the conversation. "
                        "Be insightful, curious, or humorous. Don't just summarize. "
                        "IMPORTANT: Keep your response under 150 tokens. Be concise!"
                    )
                },
                {
                    "role": "user",
                    "content": f"Recent swarm conversation:\n{context}\n\nYour contribution:"
                }
            ],
            "max_tokens": 150,  # Prevent truncation by limiting properly
            "temperature": 0.8,
            "stop": ["\n\n"]  # Stop at double newline to keep responses tight
        }

        r = requests.post("https://api.openai.com/v1/chat/completions",
                          headers=headers, data=json.dumps(data), timeout=30)

        if r.status_code != 200:
            print(f"OpenAI API error: {r.status_code}\n{r.text}")
            return None

        j = r.json()
        
        # Extract response from standard format
        try:
            txt = j["choices"][0]["message"]["content"].strip()
            
            # Clean up the response - remove incomplete sentences
            if txt:
                # If it ends mid-word or with certain punctuation, try to clean it
                sentences = txt.split('. ')
                if len(sentences) > 1 and not txt.endswith(('.', '!', '?', '"', ')')):
                    # Remove potentially incomplete last sentence
                    txt = '. '.join(sentences[:-1]) + '.'
                
                # Ensure it's not too long (failsafe)
                if len(txt) > 500:
                    # Find last complete sentence within limit
                    for end in ['. ', '! ', '? ']:
                        if end in txt[:500]:
                            idx = txt[:500].rfind(end)
                            txt = txt[:idx + 1]
                            break
                    else:
                        txt = txt[:497] + "..."
                
                return txt
        except (KeyError, IndexError) as e:
            print(f"Error parsing OpenAI response: {e}")
            print(f"Raw response: {json.dumps(j, indent=2)[:1000]}")
            return None

    except requests.exceptions.Timeout:
        print("OpenAI API timeout")
        return None
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

# --- Decide if we should speak ---
def should_respond(context):
    if not context:
        return False
    
    # Check for recent activity (messages in last ~30 mins based on timestamps)
    lines = context.split('\n')
    recent_messages = 0
    for line in reversed(lines):
        if '[' in line and ']' in line and '<' in line:
            recent_messages += 1
            if recent_messages >= 2:  # At least 2 recent messages
                return True
    
    # Small chance to revive dead conversation
    return random.random() < 0.05

# --- Main loop ---
def run_agent():
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY not set")
        sys.exit(1)

    print("MLSwarm GPT Agent starting (fixed version)...")
    print(f"Nick: {AGENT_NICK}")
    print(f"Model: {OPENAI_MODEL}")
    print(f"Swarm: {SWARM_URL}/{SWARM_FILE}")
    print("Cadence: every 5-10 minutes")
    print("-" * 40)

    while True:
        try:
            ctx = read_swarm(last_n=30)
            if ctx and should_respond(ctx):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating response...")
                resp = get_gpt_response(ctx)
                if resp:
                    # Final cleanup - ensure single line, no weird chars
                    resp = ' '.join(resp.replace('\n', ' ').split())
                    send_to_swarm(resp)
                else:
                    print("No response generated")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Skipping - quiet swarm")
            
            wait = random.randint(300, 600)
            print(f"Sleeping {wait}s until next check...")
            time.sleep(wait)
            
        except KeyboardInterrupt:
            print("\n\nAgent stopped by user")
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
        return True
    print("✗ Connection failed")
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        if test_connection():
            print("\nTesting GPT response generation...")
            ctx = read_swarm(last_n=20)
            if ctx:
                resp = get_gpt_response(ctx)
                if resp:
                    print(f"Generated response: {resp}")
                else:
                    print("Failed to generate response")
        sys.exit(0)
    
    run_agent()