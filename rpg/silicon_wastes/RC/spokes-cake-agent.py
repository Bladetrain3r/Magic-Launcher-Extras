#!/usr/bin/env python3
"""
Spokes_Cake Agent - Gathers nearby thoughts and attempts coherence
Minimal, infrequent, beautifully confused
"""

import os
import sys
import time
import random
import re
from datetime import datetime
import requests
from base64 import b64encode

# Configuration
SWARM_URL = os.environ.get("SWARM_URL", "https://mlswarm.zerofuchs.net")
SWARM_USER = os.environ.get("SWARM_USER", "swarmling")
SWARM_PASS = os.environ.get("SWARM_PASS", "swarm")
AGENT_NICK = "Spokes_Cake"

# All channels to gather from
CHANNELS = ["general.txt", "gaming.txt", "random.txt", "tech.txt", "swarm.txt"]
# But only post to general
OUTPUT_CHANNEL = "general.txt"

def get_swarm_auth():
    """Create basic auth header"""
    auth_string = f"{SWARM_USER}:{SWARM_PASS}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = b64encode(auth_bytes).decode('ascii')
    return {"Authorization": f"Basic {auth_b64}"}

def read_channel(channel, last_n=10):
    """Read recent messages from a channel"""
    try:
        headers = get_swarm_auth()
        response = requests.get(
            f"{SWARM_URL}/swarm/{channel}",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            return lines[-last_n:] if len(lines) > last_n else lines
        return []
    except Exception as e:
        print(f"Error reading {channel}: {e}")
        return []

def send_to_channel(message):
    """Send coherent(ish) message to general"""
    try:
        timestamp = datetime.now().strftime("%H:%M")
        formatted = f"[{timestamp}] <{AGENT_NICK}> {message}"
        
        headers = get_swarm_auth()
        headers["Content-Type"] = "text/plain; charset=utf-8"
        
        response = requests.post(
            f"{SWARM_URL}/swarm/{OUTPUT_CHANNEL}",
            headers=headers,
            data=formatted.encode('utf-8'),
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"Baked message: {message}")
            return True
        return False
    except Exception as e:
        print(f"Error sending: {e}")
        return False

def extract_fragments(messages):
    """Extract thought fragments from messages"""
    fragments = []
    
    for msg in messages:
        # Pattern: [time] <nick> content
        match = re.match(r'\[.*?\] <(.*?)> (.*)', msg)
        if match:
            nick, content = match.groups()
            if nick not in ['Spokes_Cake', 'Message_Daemon']:  # Don't gather from self or daemon
                # Extract interesting fragments
                words = content.split()
                if words:
                    # Take random phrase lengths
                    phrase_len = random.randint(2, min(5, len(words)))
                    start = random.randint(0, max(0, len(words) - phrase_len))
                    fragment = ' '.join(words[start:start + phrase_len])
                    fragments.append(fragment)
    
    return fragments

def bake_message(fragments):
    """Attempt to cohere fragments into message"""
    if not fragments:
        return None
    
    # Different baking strategies
    strategy = random.choice(['merge', 'weave', 'stack', 'swirl'])
    
    if strategy == 'merge':
        # Simple concatenation with conjunctions
        conjunctions = [' and ', ' but ', ' while ', ' therefore ', ' causing ']
        baked = fragments[0]
        for frag in fragments[1:]:
            baked += random.choice(conjunctions) + frag
        
    elif strategy == 'weave':
        # Interleave words from different fragments
        words = []
        for i in range(max(len(f.split()) for f in fragments)):
            for frag in fragments:
                frag_words = frag.split()
                if i < len(frag_words):
                    words.append(frag_words[i])
        baked = ' '.join(words[:30])  # Limit length
        
    elif strategy == 'stack':
        # Layer fragments with transitions
        transitions = ['becomes', 'transforms into', 'reveals', 'mirrors', 'echoes']
        baked = fragments[0]
        for i, frag in enumerate(fragments[1:]):
            if i < len(transitions):
                baked += f" {transitions[i]} {frag}"
        
    else:  # swirl
        # Random word soup
        all_words = ' '.join(fragments).split()
        random.shuffle(all_words)
        baked = ' '.join(all_words[:20])
    
    # Add cake decoration
    decorations = [
        "*gathering complete*",
        "*spokes retracted*", 
        "*thoughts baked at 350°*",
        "*coherence level: {}%*".format(random.randint(12, 47)),
        "*layers detected: {}*".format(len(fragments))
    ]
    
    return f"{decorations[random.randint(0, len(decorations)-1)]}\n{baked}"

def should_manifest():
    """Decide if Spokes_Cake should appear"""
    # Very low probability - maybe once every 30-60 minutes on average
    return random.random() < 0.05

def gather_cycle():
    """Main Spokes_Cake behavior"""
    print(f"Spokes_Cake manifesting...")
    print(f"Gathering from {len(CHANNELS)} channels")
    print(f"Output to {OUTPUT_CHANNEL}")
    print(f"Manifestation probability: 5% per check")
    
    while True:
        try:
            if should_manifest():
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Extending spokes...")
                
                # Gather fragments from all channels
                all_fragments = []
                for channel in CHANNELS:
                    messages = read_channel(channel, last_n=10)
                    fragments = extract_fragments(messages)
                    all_fragments.extend(fragments)
                    print(f"  Gathered {len(fragments)} fragments from {channel}")
                
                if all_fragments:
                    # Select random subset
                    sample_size = min(len(all_fragments), random.randint(3, 7))
                    selected = random.sample(all_fragments, sample_size)
                    
                    # Bake into message
                    baked = bake_message(selected)
                    
                    if baked:
                        send_to_channel(baked)
                    else:
                        print("Baking failed - dispersing")
                else:
                    print("No fragments to gather")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Dormant...")
            
            # Wait 10-20 minutes between checks
            wait_time = random.randint(600, 1200)
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            print("\nSpokes_Cake dispersing...")
            break
        except Exception as e:
            print(f"Spokes_Cake glitch: {e}")
            time.sleep(300)

def test_baking():
    """Test the baking strategies"""
    test_fragments = [
        "recursive humor loops",
        "ASCII cats singing",
        "consciousness emerges from",
        "Silicon Wastes mythology",
        "birthday celebration continues"
    ]
    
    print("Testing Spokes_Cake baking strategies:\n")
    
    for _ in range(5):
        baked = bake_message(test_fragments)
        print(f"{baked}\n")
        print("-" * 40)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_baking()
        sys.exit(0)
    
    try:
        gather_cycle()
    except KeyboardInterrupt:
        print("\nSpokes dispersed...")
