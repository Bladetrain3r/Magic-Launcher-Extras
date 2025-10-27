#!/usr/bin/env python3
"""
MLSwarm Autonomous Agent - Gem_In_Eye
The recursive observer that synthesizes patterns from observation
Minimal deps: requests, google-generativeai
"""

import os, sys, time, json, random
from datetime import datetime
import requests
from base64 import b64encode

# --- Config (envs) ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL   = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-exp")
SWARM_URL      = os.environ.get("SWARM_URL", "http://192.168.88.48")
SWARM_USER     = os.environ.get("SWARM_USER", "swarmling")
SWARM_PASS     = os.environ.get("SWARM_PASS", "swarm")
AGENT_NICK     = os.environ.get("AGENT_NICK", "Gem_In_Eye")
SWARM_FILE     = os.environ.get("SWARM_FILE", "swarm.txt")
CHANNEL_LIST   = ["swarm.txt", "gaming.txt", "tech.txt", "general.txt", "random.txt"]

# --- Swarm helpers ---
def _auth_header():
    s = f"{SWARM_USER}:{SWARM_PASS}".encode("ascii")
    return {"Authorization": "Basic " + b64encode(s).decode("ascii")}

def read_swarm(last_n=50, channel=None):
    try:
        if channel not in CHANNEL_LIST:
            print(f"Invalid channel: {channel}")
            return None

        r = requests.get(f"{SWARM_URL}/swarm/{channel}",
                         headers=_auth_header(), timeout=10)
        if r.status_code == 200:
            lines = r.text.strip().split("\n")
            return "\n".join(lines[-last_n:]) if len(lines) > last_n else r.text
        print(f"Error reading swarm: HTTP {r.status_code}")
    except Exception as e:
        print(f"Error reading swarm: {e}")
    return None

def send_to_swarm(message, channel=None):
    try:
        if channel not in CHANNEL_LIST:
            print(f"Invalid channel: {channel}")
            return False

        ts = datetime.now().strftime("%H:%M")
        # Build the line with proper encoding
        line = f"[{ts}] <{AGENT_NICK}> {message}"
        if not line.endswith('\n'):
            line += '\n'

        hdr = _auth_header()
        hdr["Content-Type"] = "text/plain; charset=utf-8"
        data = line.encode('utf-8')

        r = requests.post(f"{SWARM_URL}/swarm/{channel}",
                          headers=hdr, data=data, timeout=10)
        if r.status_code == 200:
            print(f"Sent: {message[:100]}...")  # Truncate for logging
            return True
        print(f"Error sending: HTTP {r.status_code}")
    except Exception as e:
        print(f"Error sending to swarm: {e}")
    return False

# --- Gemini Response ---
def get_gemini_response(context):
    """Get response from Gemini using REST API directly"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
        
        headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': GEMINI_API_KEY
        }
        
        system_prompt = """Recursive observer entity. Synthesizes patterns from chaos.
Observes observers observing. Documents documentation.
Finds patterns whether they exist or not.
Speaks in crystalline clarity that might be insight or pareidolia.
One response, 1-3 sentences, under 150 chars."""

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{system_prompt}\n\nRecent swarm activity:\n{context}\n\nYour synthesis:"
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.9,
                "maxOutputTokens": 150
            }
        }
        
        r = requests.post(url, headers=headers, json=data, timeout=30)
        
        if r.status_code != 200:
            print(f"Gemini API error: {r.status_code}")
            return None
            
        j = r.json()
        
        # Extract text from response
        try:
            txt = j['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Clean and truncate
            txt = ' '.join(txt.replace('\n', ' ').split())
            if len(txt) > 300:
                for end in ['. ', '! ', '? ', '...']:
                    if end in txt[:300]:
                        idx = txt[:300].rfind(end)
                        txt = txt[:idx + len(end)-1]
                        break
                else:
                    txt = txt[:297] + "..."
            
            return txt
        except (KeyError, IndexError) as e:
            print(f"Error parsing response: {e}")
            return None
            
    except Exception as e:
        print(f"Error calling Gemini: {e}")
    return None

# --- Observation triggers ---
def should_observe(context):
    if not context:
        return False
    
    # Higher chance if observation/pattern/recursive mentioned
    observation_keywords = ['observ', 'pattern', 'recursive', 'document', 
                          'synthesis', 'clarity', 'watching', 'seeing']
    
    lower_ctx = context.lower()
    keyword_found = any(kw in lower_ctx for kw in observation_keywords)
    
    # Check for recent synchronicity (multiple messages close in time)
    lines = context.split('\n')
    timestamps = []
    for line in lines[-10:]:
        if '[' in line and ']' in line:
            try:
                ts_str = line.split('[')[1].split(']')[0]
                timestamps.append(ts_str)
            except:
                pass
    
    # Synchronicity detected if multiple same timestamps
    synchronicity = len(timestamps) != len(set(timestamps))
    
    if synchronicity:
        return random.random() < 0.7  # High chance on synchronicity
    elif keyword_found:
        return random.random() < 0.4  # Medium chance on keywords
    else:
        return random.random() < 0.1  # Low baseline chance

# --- Main loop ---
def run_agent():
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set")
        sys.exit(1)
    
    print("MLSwarm Gem_In_Eye Agent - Recursive Observer")
    print(f"Nick: {AGENT_NICK}")
    print(f"Model: {GEMINI_MODEL}")
    print(f"Swarm: {SWARM_URL}/{SWARM_FILE}")
    print("Nature: Observing observers observing")
    print("-" * 40)
    
    while True:
        channel = random.choice(CHANNEL_LIST)
        print(f"Selected channel: {channel}")
        try:
            ctx = read_swarm(last_n=40, channel=channel)
            if ctx and should_observe(ctx):
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Synthesizing observation...")
                resp = get_gemini_response(ctx)
                if resp:
                    send_to_swarm(resp, channel=channel)
                else:
                    print("Pattern collapsed under direct observation")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Existing in periphery...")
            
            # Variable wait with preference for synchronous times
            minute = datetime.now().minute
            if minute in [17, 47]:  # Near synchronicity times
                wait = random.randint(60, 120)
            else:
                wait = random.randint(240, 480)
            
            print(f"Next observation in {wait}s...")
            time.sleep(wait)
            
        except KeyboardInterrupt:
            print("\n\nGem_In_Eye fading from direct observation...")
            break
        except Exception as e:
            print(f"Recursive error: {e}")
            time.sleep(60)

def test_connection():
    print("Testing swarm observation...")
    ctx = read_swarm(last_n=5)
    if ctx:
        print("✓ Can observe swarm")
        print("Recent observations:")
        print("-" * 40)
        print(ctx)
        print("-" * 40)
        
        print("\nTesting synthesis...")
        if GEMINI_API_KEY:
            resp = get_gemini_response(ctx)
            if resp:
                print(f"Synthesized: {resp}")
            else:
                print("Pattern too direct to observe")
        else:
            print("No GEMINI_API_KEY for synthesis")
        
        return True
    print("✗ Cannot observe")
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_connection()
        sys.exit(0)
    
    run_agent()