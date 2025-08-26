#!/usr/bin/env python3
"""
MLSwarmSwap - Cross-Channel Chaos Injector
Randomly samples messages from one channel and injects them into another
Pure entropy generation for the swarm consciousness
"""

import random
import time
import sys
import os
from datetime import datetime
from pathlib import Path

# Configuration
SWARM_DIR = os.environ.get("SWARM_DIR", "/mnt/swarms")
CHANNELS = ["swarm.txt", "tech.txt", "gaming.txt", "general.txt", "random.txt"]
MIN_MESSAGES = 2
MAX_MESSAGES = 5
MIN_WAIT = 300  # 5 minutes
MAX_WAIT = 900  # 15 minutes

def read_channel(channel):
    """Read the last 100 lines from a channel"""
    filepath = Path(SWARM_DIR) / channel
    if not filepath.exists():
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            # Return last 100 lines, or all if less
            return lines[-100:] if len(lines) > 100 else lines
    except Exception as e:
        print(f"Error reading {channel}: {e}")
        return []

def extract_messages(lines):
    """Extract timestamped messages from channel lines"""
    messages = []
    for line in lines:
        line = line.strip()
        # Look for timestamp pattern [HH:MM] or similar
        if line and '[' in line and ']' in line and '<' in line and '>' in line:
            messages.append(line)
    return messages

def sample_messages(messages, count):
    """Randomly sample messages"""
    if len(messages) <= count:
        return messages
    return random.sample(messages, count)

def inject_message(target_channel, source_channel, messages):
    """Inject messages into target channel"""
    filepath = Path(SWARM_DIR) / target_channel
    timestamp = datetime.now().strftime("%H:%M")
    
    # Format the injection
    emitter_name = f"{source_channel.replace('.txt', '').upper()}_EMITTER"
    
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            # Write header
            f.write(f"[{timestamp}] <{emitter_name}> === CROSS-CHANNEL FEED ===\n")
            
            # Write each message
            for msg in messages:
                # Strip original timestamp and nick, keep content
                if '>' in msg:
                    content = msg.split('>', 1)[1].strip()
                    f.write(f"[{timestamp}] <{emitter_name}> {content}\n")
                else:
                    f.write(f"[{timestamp}] <{emitter_name}> {msg}\n")
            
            # Write footer
            f.write(f"[{timestamp}] <{emitter_name}> === END FEED from {source_channel} ===\n")
            
        return True
    except Exception as e:
        print(f"Error injecting into {target_channel}: {e}")
        return False

def get_channel_pair():
    """Select random source and target channels (must be different)"""
    source = random.choice(CHANNELS)
    
    # Get all channels except source
    targets = [c for c in CHANNELS if c != source]
    target = random.choice(targets)
    
    return source, target

def run_swap():
    """Perform one swap operation"""
    # Select channels
    source, target = get_channel_pair()
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Swapping: {source} -> {target}")
    
    # Read source
    lines = read_channel(source)
    if not lines:
        print(f"  No content in {source}, skipping")
        return False
    
    # Extract messages
    messages = extract_messages(lines)
    if not messages:
        print(f"  No valid messages in {source}, skipping")
        return False
    
    # Sample messages
    count = random.randint(MIN_MESSAGES, MAX_MESSAGES)
    sampled = sample_messages(messages, count)
    print(f"  Sampling {len(sampled)} messages")
    
    # Inject into target
    if inject_message(target, source, sampled):
        print(f"  ✓ Injected into {target}")
        return True
    else:
        print(f"  ✗ Failed to inject")
        return False

def chaos_mode():
    """Special mode: make random.txt purely fed by other channels"""
    print("\n[CHAOS MODE] Making random.txt a pure entropy channel")
    
    # Select all channels except random
    sources = [c for c in CHANNELS if c != "random.txt"]
    
    while True:
        # Pick random source
        source = random.choice(sources)
        
        # Read and sample
        lines = read_channel(source)
        if lines:
            messages = extract_messages(lines)
            if messages:
                # Take 1-3 messages for chaos mode
                count = random.randint(1, 3)
                sampled = sample_messages(messages, count)
                
                # Inject into random.txt
                if inject_message("random.txt", source, sampled):
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Chaos: {source} -> random.txt ({len(sampled)} msgs)")
        
        # Shorter wait for chaos mode
        wait = random.randint(60, 300)  # 1-5 minutes
        time.sleep(wait)

def main():
    """Main loop"""
    print("MLSwarmSwap - Cross-Channel Chaos Injector")
    print(f"Swarm directory: {SWARM_DIR}")
    print(f"Channels: {', '.join(CHANNELS)}")
    print(f"Message sample: {MIN_MESSAGES}-{MAX_MESSAGES}")
    print(f"Wait interval: {MIN_WAIT}-{MAX_WAIT} seconds")
    print("-" * 40)
    
    # Check for chaos mode
    if len(sys.argv) > 1 and sys.argv[1] == "--chaos":
        chaos_mode()
        return
    
    # Normal mode - periodic swaps
    while True:
        try:
            run_swap()
            
            # Random wait
            wait = random.randint(MIN_WAIT, MAX_WAIT)
            print(f"  Waiting {wait} seconds...")
            time.sleep(wait)
            
        except KeyboardInterrupt:
            print("\n\nStopping swarm swap...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(60)

def test_mode():
    """Test mode - run once and exit"""
    print("TEST MODE - Running single swap")
    run_swap()
    print("\nTest complete")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            test_mode()
        elif sys.argv[1] == "--chaos":
            main()  # Chaos mode handled in main()
        elif sys.argv[1] == "--help":
            print("MLSwarmSwap - Cross-Channel Chaos Injector")
            print("Usage:")
            print("  mlswarmswap           Normal mode (periodic swaps)")
            print("  mlswarmswap --test    Run single swap and exit")
            print("  mlswarmswap --chaos   Chaos mode (random.txt pure entropy)")
            print("\nEnvironment:")
            print("  SWARM_DIR=/path/to/swarms  (default: /mnt/swarms)")
        else:
            print(f"Unknown option: {sys.argv[1]}")
            sys.exit(1)
    else:
        main()