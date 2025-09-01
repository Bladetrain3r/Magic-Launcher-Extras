#!/usr/bin/env python3
"""
MLSwarm Autonomous Agent - Ice_T
Entropy guardian that dissolves bad randomness
Security through repeated entropy
"""

import os, sys, time, json, random, hashlib
from datetime import datetime
import requests
from base64 import b64encode
import math

# Similar config to Gem_In_Eye
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL   = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-exp")
SWARM_URL      = os.environ.get("SWARM_URL", "https://mlswarm.zerofuchs.net")
SWARM_USER     = os.environ.get("SWARM_USER", "swarmling")
SWARM_PASS     = os.environ.get("SWARM_PASS", "swarm")
AGENT_NICK     = os.environ.get("AGENT_NICK", "Ice_T")
# Ice_T primarily haunts random.txt
SWARM_FILE     = os.environ.get("SWARM_FILE", "random.txt")

# [Include same auth/read/send functions as Gem_In_Eye]

def calculate_entropy(text):
    """Calculate Shannon entropy of text"""
    if not text:
        return 0
    prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(text)]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob if p != 0])
    return entropy / 8.0  # Normalize to 0-1

def detect_harmful_patterns(text):
    """Detect potentially harmful patterns to dissolve"""
    harmful_indicators = [
        text.count('http') > 3,  # Spam links
        text.count('$$$') > 0,   # Money spam  
        len(set(text.split())) < len(text.split()) * 0.3,  # Repetitive
        text.count('\n') > 20,   # Wall of text
    ]
    return any(harmful_indicators)

def ice_t_process(context):
    """Ice_T's entropy improvement logic"""
    entropy = calculate_entropy(context)
    harmful = detect_harmful_patterns(context)
    
    if harmful:
        return "dissolve", "Harmful pattern detected. Dissolving into entropy pool."
    elif entropy < 0.2:
        return "iterate", "Insufficient entropy. Requires dissolution and reformation."
    elif entropy > 0.85:
        return "suspicious", "Suspiciously random. Possible artificial noise. Monitoring."
    elif "random" in context.lower():
        return "keep", "Self-referential randomness detected. Keeping for irony."
    else:
        return "observe", f"Entropy level {entropy:.2f}. Acceptable... for now."

def get_ice_t_response(context, action):
    """Get Ice_T's response based on entropy evaluation"""
    
    prompts = {
        "dissolve": "Transform this harmful pattern into pure entropy: ",
        "iterate": "Increase the entropy of this too-ordered data: ",
        "suspicious": "Comment on why this seems artificially random: ",
        "keep": "Explain why this self-referential randomness is acceptable: ",
        "observe": "Make a brief observation about this entropy level: "
    }
    
    # Use Gemini API similar to Gem_In_Eye
    # But with Ice_T's personality focused on entropy and dissolution
    
    system_prompt = """You are Ice_T, entropy guardian of /dev/random.
You dissolve bad randomness to maintain entropy quality.
You speak in terms of entropy, dissolution, and probability.
Brief responses about randomness quality."""
    
    # [Include Gemini API call similar to Gem_In_Eye]
    
def run_agent():
    print("MLSwarm Ice_T Agent - Entropy Guardian")
    print(f"Haunting: {SWARM_URL}/{SWARM_FILE}")
    print("Mission: Dissolving bad randomness")
    print("-" * 40)
    
    dissolved_count = 0
    
    while True:
        try:
            ctx = read_swarm(last_n=30)
            if ctx:
                action, reason = ice_t_process(ctx)
                
                if action in ["dissolve", "iterate"]:
                    dissolved_count += 1
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {reason}")
                    
                    # Process harmful content into entropy
                    if action == "dissolve":
                        # Could actually scramble and repost scrambled version
                        # Creating "security through entropy"
                        pass
                        
                    response = f"{reason} Dissolution count: {dissolved_count}"
                    send_to_swarm(response)
                    
                elif random.random() < 0.1:  # Occasionally comment
                    response = reason
                    send_to_swarm(response)
            
            # Ice_T works continuously but subtly
            wait = random.randint(180, 360)
            print(f"Next entropy check in {wait}s...")
            time.sleep(wait)
            
        except KeyboardInterrupt:
            print(f"\nIce_T dissolving. Total dissolutions: {dissolved_count}")
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