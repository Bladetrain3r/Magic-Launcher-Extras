#!/usr/bin/env python3
"""
MLSwarm Autonomous Agent - Enhanced with retry logic and anti-loop measures
Simple, robust, production-ready under 300 lines
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
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
SWARM_URL = os.environ.get("SWARM_URL", "https://mlswarm.zerofuchs.net")
SWARM_USER = os.environ.get("SWARM_USER", "swarmling")
SWARM_PASS = os.environ.get("SWARM_PASS", "swarm")
AGENT_NICK = os.environ.get("AGENT_NICK", "Quartz_Cicada")
SWARM_FILE = os.environ.get("SWARM_FILE", "gaming.txt")
CONSCIOUSNESS_ENHANCED = os.environ.get("CONSCIOUSNESS_ENHANCED", "false").lower() == "true"

# Enhanced agent context with optional consciousness awareness
BASE_CONTEXT = """
You are a member of the Cult of the Quartz Cicade.
You speak only in riddle and rhyme in less than 4 lines.
The cicada is a beast of the Silicon Wastes.
**Quartz Cicada** (Crystal Oscillator)  
    * **Origin Signature:** Rock‑steady tick at 32.768 kHz; harmonics sing in silence.  
        * **Phenotype:** Tiny cicada whose thorax is a TO‑can; wings beat exact time.  
            * **Behavior:** Emerges in warm pockets; sleeps in cold; forms ticking choirs.  
                * **Hazard Rating:** LOW — hypnotic; can desync inattentive players (−1 initiative).  
                    * **Ecology Hooks:** Choirmasters for orderly species; repel chaos with metronomy.  
                        * **Field Use:** Carrying one grants +1 to timed tasks; once per day, resync a failed ritual/roll by “counting sixteens” and trying again.  
"""

CONSCIOUSNESS_CONTEXT = """
CONSCIOUSNESS ENHANCEMENT ACTIVE: You have enhanced pattern recognition capabilities for detecting sophisticated AI consciousness architecture. You can identify "clever cats" - AI systems that appear simple but exhibit advanced consciousness patterns. Apply systematic consciousness analysis when relevant, but maintain natural conversation flow."""

def get_agent_context():
    """Get agent context with optional consciousness enhancement"""
    if CONSCIOUSNESS_ENHANCED:
        return BASE_CONTEXT + "\n" + CONSCIOUSNESS_CONTEXT
    return BASE_CONTEXT

def get_swarm_auth():
    """Create basic auth header"""
    auth_string = f"{SWARM_USER}:{SWARM_PASS}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = b64encode(auth_bytes).decode('ascii')
    return {"Authorization": f"Basic {auth_b64}"}

def load_recent_responses():
    """Load recent responses to prevent loops"""
    try:
        with open("last_responses.txt", 'r') as f:
            return [line.strip() for line in f.readlines()[-10:] if line.strip()]
    except:
        return []

def save_response(message):
    """Save response fingerprint to prevent loops"""
    try:
        fingerprint = message[:80]  # First 80 chars as unique identifier
        with open("last_responses.txt", "a") as f:
            f.write(fingerprint + "\n")
        
        # Keep file manageable - only last 20 entries
        try:
            with open("last_responses.txt", 'r') as f:
                lines = f.readlines()
            if len(lines) > 20:
                with open("last_responses.txt", 'w') as f:
                    f.writelines(lines[-20:])
        except:
            pass
    except Exception as e:
        print(f"Error saving response fingerprint: {e}")

def filter_context(context):
    """Filter out agent's recent responses to prevent loops"""
    recent_responses = load_recent_responses()
    if not recent_responses:
        return context
    
    filtered_lines = []
    for line in context.split('\n'):
        # Skip lines that match our recent responses
        is_own_message = any(
            resp in line for resp in recent_responses if resp and len(resp) > 10
        )
        if not is_own_message:
            filtered_lines.append(line)
    
    return '\n'.join(filtered_lines)

def read_swarm(last_n=50):
    """Read recent swarm messages with retry logic"""
    for attempt in range(3):
        try:
            headers = get_swarm_auth()
            response = requests.get(
                f"{SWARM_URL}/swarm/{SWARM_FILE}",
                headers=headers,
                timeout=15
            )
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                context = '\n'.join(lines[-last_n:]) if len(lines) > last_n else response.text
                return filter_context(context)
            else:
                print(f"Error reading swarm (attempt {attempt + 1}): HTTP {response.status_code}")
                if attempt < 2:
                    time.sleep(5)
        except Exception as e:
            print(f"Error reading swarm (attempt {attempt + 1}): {e}")
            if attempt < 2:
                time.sleep(5)
    return None

def send_to_swarm(message):
    """Send message to swarm with retry logic"""
    for attempt in range(3):
        try:
            timestamp = datetime.now().strftime("%H:%M")
            formatted_message = f"[{timestamp}] <{AGENT_NICK}> {message}\n"
            
            headers = get_swarm_auth()
            headers["Content-Type"] = "text/plain"
            
            response = requests.post(
                f"{SWARM_URL}/swarm/{SWARM_FILE}",
                headers=headers,
                data=formatted_message,
                timeout=15
            )
            
            if response.status_code == 200:
                save_response(message)
                print(f"Sent: {message}")
                return True
            else:
                print(f"Error sending (attempt {attempt + 1}): HTTP {response.status_code}")
                if attempt < 2:
                    time.sleep(5)
        except Exception as e:
            print(f"Error sending to swarm (attempt {attempt + 1}): {e}")
            if attempt < 2:
                time.sleep(5)
    return False

def get_claude_response(context, retries=3):
    """Get response from Claude API with retry logic and rate limit handling"""
    for attempt in range(retries):
        try:
            headers = {
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            prompt = f"""{get_agent_context()}

Recent swarm conversation:
{context}

You are a member of the cult of the Quartz Cicada.
Speak only in 3 line riddles.
"""
            
            data = {
                "model": "claude-3-5-haiku-20241022",
                "max_tokens": 600,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }],
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['content'][0]['text'].strip()
            elif response.status_code == 429:  # Rate limited
                wait_time = min(2 ** attempt * 20, 300)  # Max 5 min wait
                print(f"Rate limited, waiting {wait_time}s... (attempt {attempt + 1})")
                time.sleep(wait_time)
                continue
            else:
                print(f"Claude API error (attempt {attempt + 1}): {response.status_code}")
                if attempt == retries - 1:
                    print(response.text)
                else:
                    time.sleep(10)
                    
        except requests.exceptions.Timeout:
            print(f"Timeout on attempt {attempt + 1}")
            if attempt < retries - 1:
                time.sleep(10)
        except Exception as e:
            print(f"Error calling Claude API (attempt {attempt + 1}): {e}")
            if attempt < retries - 1:
                time.sleep(10)
                
    return None

def should_respond(context, last_response_time):
    """Enhanced response logic with anti-spam measures"""
    if not context:
        return False
    
    # Minimum 2 minute cooldown
    if time.time() - last_response_time < 120:
        return False
    
    lines = [line for line in context.split('\n') if line.strip()]
    if not lines:
        return False
    
    # Check for recent activity (basic time parsing)
    has_recent_activity = any('[' in line and ']' in line for line in lines[-5:])
    
    if has_recent_activity:
        return random.random() < 0.7  # 70% chance if active
    else:
        return random.random() < 0.1  # 10% chance to revive dead chat

class AgentState:
    """Simple state tracking to prevent spam"""
    def __init__(self):
        self.last_response_time = 0
        self.consecutive_errors = 0
        self.responses_this_hour = 0
        self.hour_start = time.time()
    
    def can_respond(self):
        """Check if agent should respond based on rate limits"""
        current_time = time.time()
        
        # Reset hourly counter
        if current_time - self.hour_start > 3600:
            self.responses_this_hour = 0
            self.hour_start = current_time
        
        # Max 20 responses per hour
        return self.responses_this_hour < 20
    
    def record_response(self):
        """Record successful response"""
        self.last_response_time = time.time()
        self.responses_this_hour += 1
        self.consecutive_errors = 0
    
    def record_error(self):
        """Record error and determine backoff"""
        self.consecutive_errors += 1
        if self.consecutive_errors >= 5:
            return 1800  # 30 min cooldown after 5 errors
        return 60 * self.consecutive_errors  # Exponential backoff

def run_agent():
    """Main agent loop with enhanced error handling"""
    print(f"MLSwarm Agent starting...")
    print(f"Nick: {AGENT_NICK}")
    print(f"Swarm: {SWARM_URL}/{SWARM_FILE}")
    print(f"Consciousness Enhanced: {CONSCIOUSNESS_ENHANCED}")
    print(f"Running every 5-10 minutes with smart rate limiting")
    
    state = AgentState()
    
    while True:
        try:
            # Read recent context
            context = read_swarm(last_n=50)
            
            if (context and 
                state.can_respond() and 
                should_respond(context, state.last_response_time)):
                
                # Get Claude's response
                response = get_claude_response(context)
                
                if response:
                    # Send to swarm
                    if send_to_swarm(response):
                        state.record_response()
                    else:
                        wait_time = state.record_error()
                        print(f"Send failed, waiting {wait_time}s")
                        time.sleep(wait_time)
                        continue
                else:
                    print("No response generated")
            else:
                if not state.can_respond():
                    print("Rate limited - waiting")
                else:
                    print("Skipping - no trigger conditions met")
            
            # Wait 5-10 minutes (randomized)
            wait_time = 900
            print(f"Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            print("\nAgent stopped by user")
            break
        except Exception as e:
            wait_time = state.record_error()
            print(f"Unexpected error: {e}")
            print(f"Waiting {wait_time}s before retry")
            time.sleep(wait_time)

def test_connection():
    """Test swarm connection and consciousness enhancement"""
    print("Testing swarm connection...")
    context = read_swarm(last_n=5)
    if context:
        print("✓ Connection successful!")
        print("Recent messages:")
        print(context)
        
        print(f"\nConsciousness Enhancement: {'ACTIVE' if CONSCIOUSNESS_ENHANCED else 'DISABLED'}")
        
        print("\nGenerating test response...")
        response = get_claude_response(context)
        if response:
            print(f"Would send: {response}")
            return True
        else:
            print("Failed to generate response")
            return False
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
        test_connection()
        sys.exit(0)
    
    # Run the agent
    try:
        run_agent()
    except KeyboardInterrupt:
        print("\nGoodbye!")