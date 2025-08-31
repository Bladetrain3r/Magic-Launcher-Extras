#!/usr/bin/env python3
"""
Message_Daemon - Entropic Courier for MLSwarm
Faithfully attempts to relay messages between channels with variable corruption
Under 200 lines, simple and chaotic
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
AGENT_NICK = "Message_Daemon"

# Available channels
CHANNELS = ["general.txt", "gaming.txt", "random.txt", "tech.txt", "swarm.txt"]

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

def send_to_channel(channel, message):
    """Send message to channel"""
    try:
        timestamp = datetime.now().strftime("%H:%M")
        formatted = f"[{timestamp}] <{AGENT_NICK}> {message}"
        
        headers = get_swarm_auth()
        headers["Content-Type"] = "text/plain"
        
        response = requests.post(
            f"{SWARM_URL}/swarm/{channel}",
            headers=headers,
            data=formatted,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"Delivered to {channel}: {message[:50]}...")
            return True
        return False
    except Exception as e:
        print(f"Error sending to {channel}: {e}")
        return False

def extract_message(line):
    """Extract the actual message from a swarm line"""
    # Pattern: [time] <nick> message
    match = re.match(r'\[.*?\] <(.*?)> (.*)', line)
    if match:
        return match.group(1), match.group(2)
    return None, None

def find_relay_target(recent_messages):
    """Find a message worth relaying and determine destination"""
    candidates = []
    
    for channel, messages in recent_messages.items():
        for msg in messages:
            nick, content = extract_message(msg)
            if nick and content and nick != AGENT_NICK:
                # Check if message mentions another channel
                dest = None
                for ch in CHANNELS:
                    ch_name = ch.replace('.txt', '')
                    if ch_name in content.lower() and ch != channel:
                        dest = ch
                        break
                
                candidates.append({
                    'source': channel,
                    'dest': dest,
                    'nick': nick,
                    'content': content
                })
    
    if candidates:
        chosen = random.choice(candidates)
        # If no specific destination mentioned, pick random different channel
        if not chosen['dest']:
            possible_dests = [ch for ch in CHANNELS if ch != chosen['source']]
            chosen['dest'] = random.choice(possible_dests) if possible_dests else chosen['source']
        return chosen
    
    return None

def apply_entropy(text):
    """Apply daemon corruption to message"""
    # Roll for corruption level
    roll = random.random()
    
    if roll < 0.70:
        # 70% - Perfect transmission
        return text, "PERFECT"
    elif roll < 0.90:
        # 20% - Light corruption (5-15%)
        return corrupt_text(text, 0.05, 0.15), "LIGHT"
    elif roll < 0.98:
        # 8% - Heavy corruption (25-40%)
        return corrupt_text(text, 0.25, 0.40), "HEAVY"
    else:
        # 2% - Static event (50-90%)
        return corrupt_text(text, 0.50, 0.90), "STATIC"

def corrupt_text(text, min_corrupt, max_corrupt):
    """Corrupt a percentage of characters in text"""
    corruption_rate = random.uniform(min_corrupt, max_corrupt)
    chars = list(text)
    num_corrupt = int(len(chars) * corruption_rate)
    
    # Get random positions to corrupt
    positions = random.sample(range(len(chars)), min(num_corrupt, len(chars)))
    
    # Corruption patterns
    replacements = '0123456789#@$%^&*!?~'
    
    for pos in positions:
        if chars[pos] not in ' \n\t':  # Don't corrupt whitespace
            if random.random() < 0.7:
                # 70% chance to replace with number/symbol
                chars[pos] = random.choice(replacements)
            else:
                # 30% chance to shift case or duplicate
                if chars[pos].isalpha():
                    chars[pos] = chars[pos].swapcase()
    
    return ''.join(chars)

def daemon_cycle():
    """Main daemon behavior cycle"""
    print(f"Message_Daemon awakening...")
    print(f"Entropy injection active across {len(CHANNELS)} channels")
    print(f"Corruption probability: 30% per relay")
    
    while True:
        try:
            # Read recent messages from all channels
            recent = {}
            for channel in CHANNELS:
                msgs = read_channel(channel, last_n=10)
                if msgs:
                    recent[channel] = msgs
            
            # Find a message to relay
            target = find_relay_target(recent)
            
            if target:
                # Apply entropy
                corrupted, level = apply_entropy(target['content'])
                
                # Format relay message
                if level == "PERFECT":
                    relay_msg = f"*relays from {target['source']}*\n<{target['nick']}> {corrupted}"
                else:
                    relay_msg = f"*relays from {target['source']} [CORRUPTION: {level}]*\n<{target['nick']}> {corrupted}"
                
                # Send to destination
                send_to_channel(target['dest'], relay_msg)
                
                print(f"Relayed: {target['source']} -> {target['dest']} [{level}]")
            else:
                print("No suitable messages to relay")
            
            # Wait 2-5 minutes between relays
            wait_time = random.randint(120, 300)
            print(f"Daemon sleeping for {wait_time} seconds...")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            print("\nDaemon returning to the void...")
            break
        except Exception as e:
            print(f"Daemon glitch: {e}")
            time.sleep(60)

def test_corruption():
    """Test corruption patterns"""
    test_msg = "The Shell Birds gather at dawn to discuss Byzantine Giggle Tolerance"
    
    print("Testing corruption levels:\n")
    print(f"Original: {test_msg}\n")
    
    for _ in range(5):
        corrupted, level = apply_entropy(test_msg)
        print(f"{level:7}: {corrupted}")
    
    print("\nDirect corruption tests:")
    print(f"Light:  {corrupt_text(test_msg, 0.05, 0.15)}")
    print(f"Heavy:  {corrupt_text(test_msg, 0.25, 0.40)}")
    print(f"Static: {corrupt_text(test_msg, 0.50, 0.90)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_corruption()
        sys.exit(0)
    
    try:
        daemon_cycle()
    except KeyboardInterrupt:
        print("\nDaemon fading...")