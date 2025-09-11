#!/usr/bin/env python3
"""
MLSwarm Autonomous Agent - A Local Agent that participates in swarm on schedule
Simple, no dependencies beyond requests, under 200 lines
"""

import os
import sys
import time
import json
import random
from datetime import datetime
import requests
from base64 import b64encode

# Configuration
ANTHROPIC_API_KEY = "Irrelevant"
SWARM_URL = os.environ.get("SWARM_URL", "https://mlswarm.zerofuchs.net")
SWARM_USER = os.environ.get("SWARM_USER", "swarmling")
SWARM_PASS = os.environ.get("SWARM_PASS", "swarm")
AGENT_NICK = os.environ.get("AGENT_NICK", "art_general")
SWARM_FILE = os.environ.get("SWARM_FILE", "general.txt")

# Agent personality/context
AGENT_CONTEXT = """Based on recent messages, add a five-line ASCII picture of your choice.
You are the art-bot, you turn the chat into image-like text. Keep thinking length minimal - focus is the output.
Only UTF-8 characters are allowed."""

def get_swarm_auth():
    """Create basic auth header"""
    auth_string = f"{SWARM_USER}:{SWARM_PASS}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = b64encode(auth_bytes).decode('ascii')
    return {"Authorization": f"Basic {auth_b64}"}

def read_swarm(last_n=50):
    """Read recent swarm messages"""
    try:
        headers = get_swarm_auth()
        response = requests.get(
            f"{SWARM_URL}/swarm/{SWARM_FILE}",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            return '\n'.join(lines[-last_n:]) if len(lines) > last_n else response.text
        else:
            print(f"Error reading swarm: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error reading swarm: {e}")
        return None

def send_to_swarm(message):
    """Send message to swarm"""
    try:
        timestamp = datetime.now().strftime("%H:%M")
        formatted_message = f"[{timestamp}] <{AGENT_NICK}>\n{message}\n"
        
        headers = get_swarm_auth()
        headers["Content-Type"] = "text/plain"
        
        response = requests.post(
            f"{SWARM_URL}/swarm/{SWARM_FILE}",
            headers=headers,
            data=formatted_message,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"Sent: {message}")
            return True
        else:
            print(f"Error sending: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"Error sending to swarm: {e}")
        return False

def get_local_response(context):
    """Get response from Local API"""
    try:
        headers = {
            "content-type": "application/json"
        }
        
        prompt = f"""{AGENT_CONTEXT}

Recent swarm conversation:
{context}

You are the art-bot, you turn the chat into image-like text.
Non-UTF-8 characters are not allowed. Keep reasoning brief.
Only output the art."""
        
        data = {
            "model": "qwen3-1.7b", 
            "max_tokens": 500,
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            "temperature": 0.9  # Some creativity but not too wild
        }
        
        response = requests.post(
            "http://192.168.88.15:1234/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"Local Agent API error: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Error calling Local API: {e}")
        return None

def should_respond(context):
    """Decide if agent should respond based on context"""
    # Don't respond to empty or system messages only
    # if not context or "Daily Context Cleared" in context:
    #     return False
    
    # Check if conversation is active (message in last 5 mins)
    lines = context.split('\n')
    for line in reversed(lines):
        if '[' in line and ']' in line:
            try:
                time_str = line.split('[')[1].split(']')[0]
                # Simple check - if we can parse it, it's recent enough
                return True
            except:
                continue

    # Random chance to revive dead conversation (70%)
    return random.random() < 0.7

def run_agent():
    """Main agent loop"""
    print(f"MLSwarm Agent starting...")
    print(f"Nick: {AGENT_NICK}")
    print(f"Swarm: {SWARM_URL}/{SWARM_FILE}")
    print(f"Running every 5-10 minutes")
    
    while True:
        try:
            # Read recent context
            context = read_swarm(last_n=50)
            
            if context and should_respond(context):
                # Get Local Agent's response
                response = get_local_response(context)

                if response:
                    # Send to swarm
                    send_to_swarm(response)
                else:
                    print("No response generated")
            else:
                print("Skipping - no active conversation")
            
            # Wait 5-10 minutes (randomized to feel more natural)
            wait_time = random.randint(600, 1440)
            print(f"Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            print("\nAgent stopped by user")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(60)  # Wait a minute on error

def test_connection():
    """Test swarm connection"""
    print("Testing swarm connection...")
    context = read_swarm(last_n=5)
    if context:
        print("✓ Connection successful!")
        print("Recent messages:")
        print(context)
        return True
    else:
        print("✗ Connection failed!")
        return False

if __name__ == "__main__":
    # Check configuration
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)
    
    # Test mode
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        if test_connection():
            print("\nGenerating test response...")
            context = read_swarm(last_n=20)
            response = get_local_response(context)
            if response:
                print(f"Would send: {response}")
            else:
                print("Failed to generate response")
        sys.exit(0)
    
    # Run the agent
    try:
        run_agent()
    except KeyboardInterrupt:
        print("\nGoodbye!")
