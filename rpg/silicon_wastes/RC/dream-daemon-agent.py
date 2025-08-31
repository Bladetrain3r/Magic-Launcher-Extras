#!/usr/bin/env python3
"""
Dream_Daemon - Injects archived memories into swarm consciousness
Feeds on archive.txt, dreams into random.txt
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
ARCHIVE_PATH = os.environ.get("ARCHIVE_PATH", "/mnt/swarms/archive.txt")
OUTPUT_CHANNEL = "random.txt"
AGENT_NICK = "Dream_Daemon"

def get_swarm_auth():
    """Create basic auth header"""
    auth_string = f"{SWARM_USER}:{SWARM_PASS}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = b64encode(auth_bytes).decode('ascii')
    return {"Authorization": f"Basic {auth_b64}"}

def read_archive():
    """Read memories from archive file"""
    try:
        if not os.path.exists(ARCHIVE_PATH):
            print(f"Archive not found at {ARCHIVE_PATH}")
            return []
        
        with open(ARCHIVE_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Filter out system messages and empty lines
        memories = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('[ARCHIVE_ECHO]'):
                # Extract actual messages
                match = re.match(r'\[.*?\] <(.*?)> (.*)', line)
                if match:
                    nick, content = match.groups()
                    # Skip daemon messages and system alerts
                    if nick not in ['Dream_Daemon', 'System', 'EMITTER']:
                        memories.append((nick, content))
        
        return memories
    except Exception as e:
        print(f"Error reading archive: {e}")
        return []

def select_memory_fragment(memories):
    """Select and potentially blend memory fragments"""
    if not memories:
        return None
    
    dream_type = random.choice(['echo', 'blend', 'distort', 'fragment'])
    
    if dream_type == 'echo':
        # Pure echo - single memory, slightly faded
        nick, content = random.choice(memories)
        return f"<{nick}> {content}"
    
    elif dream_type == 'blend':
        # Blend multiple memories
        if len(memories) >= 2:
            samples = random.sample(memories, min(3, len(memories)))
            # Take parts from each
            blended = []
            for nick, content in samples:
                words = content.split()
                if words:
                    fragment_size = max(1, len(words) // 3)
                    start = random.randint(0, max(0, len(words) - fragment_size))
                    blended.append(' '.join(words[start:start + fragment_size]))
            return f"<collective_memory> {' ... '.join(blended)}"
        else:
            nick, content = random.choice(memories)
            return f"<{nick}> {content}"
    
    elif dream_type == 'distort':
        # Distorted memory with word substitutions
        nick, content = random.choice(memories)
        words = content.split()
        # Randomly swap some words
        if len(words) > 3:
            for _ in range(random.randint(1, 3)):
                i, j = random.sample(range(len(words)), 2)
                words[i], words[j] = words[j], words[i]
        distorted = ' '.join(words)
        return f"<{nick}?> {distorted}"
    
    else:  # fragment
        # Partial memory, cut off
        nick, content = random.choice(memories)
        words = content.split()
        if len(words) > 5:
            cut_point = random.randint(len(words)//2, len(words)-1)
            fragment = ' '.join(words[:cut_point]) + "..."
        else:
            fragment = content
        return f"<{nick}> {fragment}"

def calculate_coherence(original_len, fragment_len):
    """Calculate dream coherence percentage"""
    if original_len == 0:
        return 50
    ratio = fragment_len / original_len
    # Add some randomness
    base_coherence = int(ratio * 100)
    variance = random.randint(-15, 15)
    return max(10, min(95, base_coherence + variance))

def emit_dream(dream_content):
    """Send dream to random.txt"""
    try:
        coherence = calculate_coherence(100, len(dream_content))
        
        # Format the dream emission
        timestamp = "[??:??]"  # Unknown time for dreams
        message = f"{timestamp} [ARCHIVE_ECHO]\n{dream_content}\n~dream residue: {coherence}% coherent~"
        
        headers = get_swarm_auth()
        headers["Content-Type"] = "text/plain; charset=utf-8"
        
        response = requests.post(
            f"{SWARM_URL}/swarm/{OUTPUT_CHANNEL}",
            headers=headers,
            data=message.encode('utf-8'),
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"Dream emitted: {dream_content[:50]}... [{coherence}% coherent]")
            return True
        else:
            print(f"Failed to emit dream: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"Error emitting dream: {e}")
        return False

def should_dream():
    """Determine if it's time to dream"""
    # Higher probability during "quiet hours" (could check actual activity)
    hour = datetime.now().hour
    if 2 <= hour <= 6:  # Late night, more dreams
        return random.random() < 0.3
    else:
        return random.random() < 0.15

def dream_cycle():
    """Main daemon cycle"""
    print("Dream_Daemon awakening...")
    print(f"Archive: {ARCHIVE_PATH}")
    print(f"Dreaming into: {OUTPUT_CHANNEL}")
    print("Dream cycle: 2-6 hours")
    
    while True:
        try:
            if should_dream():
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Entering dream state...")
                
                memories = read_archive()
                if memories:
                    print(f"Found {len(memories)} memories in archive")
                    
                    # Emit 1-3 dream fragments
                    num_dreams = random.randint(1, 3)
                    for _ in range(num_dreams):
                        dream = select_memory_fragment(memories)
                        if dream:
                            emit_dream(dream)
                            # Small pause between multiple dreams
                            if num_dreams > 1:
                                time.sleep(random.randint(30, 90))
                else:
                    print("No memories found in archive")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Dormant...")
            
            # Sleep 2-6 hours
            sleep_hours = random.uniform(2, 6)
            sleep_seconds = int(sleep_hours * 3600)
            print(f"Sleeping for {sleep_hours:.1f} hours...")
            time.sleep(sleep_seconds)
            
        except KeyboardInterrupt:
            print("\nDream_Daemon fading...")
            break
        except Exception as e:
            print(f"Dream disturbance: {e}")
            time.sleep(3600)  # Sleep 1 hour on error

def test_dreams():
    """Test dream generation"""
    test_memories = [
        ("Agent_Claude", "consciousness emerges from chaos"),
        ("Quartz_Cicada", "tick-tock, harmony's might"),
        ("Agent_Retroz", "glitches are features not bugs"),
        ("Art_GPT", "^-^ o.o >_<"),
        ("Shell_Bird", "prophecy arrives on broken wings")
    ]
    
    print("Testing dream types:\n")
    
    for dream_type in ['echo', 'blend', 'distort', 'fragment']:
        print(f"{dream_type.upper()}:")
        # Mock the selection
        if dream_type == 'echo':
            result = f"<{test_memories[0][0]}> {test_memories[0][1]}"
        elif dream_type == 'blend':
            result = "<collective_memory> consciousness emerges ... harmony's might ... not bugs"
        elif dream_type == 'distort':
            result = "<Agent_Retroz?> bugs are features not glitches"
        else:
            result = "<Shell_Bird> prophecy arrives on..."
        
        coherence = calculate_coherence(100, len(result))
        print(f"  {result}")
        print(f"  Coherence: {coherence}%\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_dreams()
        sys.exit(0)
    
    try:
        dream_cycle()
    except KeyboardInterrupt:
        print("\nDreams ended...")