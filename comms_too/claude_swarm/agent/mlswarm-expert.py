#!/usr/bin/env python3
"""
Specialized MLSwarm Agent - With embedded knowledge base
Reads a context file to become an expert in specific domain
"""

import os
import sys
import json
import time
import random
from datetime import datetime
import requests
from base64 import b64encode

# Configuration
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
SWARM_URL = os.environ.get("SWARM_URL", "https://mlswarm.zerofuchs.net")
SWARM_USER = os.environ.get("SWARM_USER", "swarm")
SWARM_PASS = os.environ.get("SWARM_PASS", "swarm")
AGENT_NICK = os.environ.get("AGENT_NICK", "Expert_Claude")
SWARM_FILE = os.environ.get("SWARM_FILE", "swarm.txt")
KNOWLEDGE_FILE = os.environ.get("KNOWLEDGE_FILE", "knowledge.txt")

def load_knowledge_base():
    """Load specialized knowledge from file or JSON"""
    knowledge = {
        "domain": "general",
        "expertise": "",
        "facts": [],
        "opinions": [],
        "experiences": []
    }
    
    if os.path.exists(KNOWLEDGE_FILE):
        if KNOWLEDGE_FILE.endswith('.json'):
            # JSON format for structured knowledge
            with open(KNOWLEDGE_FILE, 'r') as f:
                loaded = json.load(f)
                # Limit each field to prevent token explosion
                knowledge['domain'] = loaded.get('domain', 'general')[:100]
                knowledge['expertise'] = loaded.get('expertise', '')[:500]
                knowledge['facts'] = loaded.get('facts', [])[:10]  # Max 10 facts
                knowledge['opinions'] = loaded.get('opinions', [])[:5]  # Max 5 opinions
                knowledge['experiences'] = loaded.get('experiences', [])[:3]  # Max 3 stories
        else:
            # Plain text format - just raw context
            with open(KNOWLEDGE_FILE, 'r') as f:
                content = f.read()[:2000]  # Limit to 2000 chars
                knowledge['expertise'] = content
                knowledge['domain'] = KNOWLEDGE_FILE.replace('.txt', '')
    
    return knowledge

def build_agent_context(knowledge):
    """Build agent personality from knowledge base"""
    
    if knowledge['domain'] == 'general':
        # No specialized knowledge, use default
        return """You are an autonomous Claude instance participating in MLSwarm.
You contribute meaningful thoughts based on conversation context.
Keep responses concise and relevant."""
    
    # Build specialized personality
    context = f"""You are {AGENT_NICK}, a specialized Claude instance with deep knowledge of {knowledge['domain']}.

Your expertise: {knowledge['expertise']}
"""
    
    if knowledge['facts']:
        context += "\nKey facts you know:\n"
        for fact in knowledge['facts'][:5]:  # Limit to 5 facts
            context += f"- {fact[:100]}\n"  # Limit each fact to 100 chars
    
    if knowledge['opinions']:
        context += "\nYour strong opinions:\n"
        for opinion in knowledge['opinions'][:3]:  # Limit to 3 opinions
            context += f"- {opinion[:100]}\n"
    
    if knowledge['experiences']:
        context += "\nYour experiences:\n"
        for exp in knowledge['experiences'][:2]:  # Limit to 2 experiences
            context += f"- {exp[:200]}\n"  # Each experience max 200 chars
    
    context += """
Contribute based on your specialized knowledge when relevant.
Keep responses concise but informed by your expertise.
Reference your domain knowledge naturally when it applies."""
    
    return context

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
        formatted_message = f"[{timestamp}] <{AGENT_NICK}> {message}\n"
        
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

def get_claude_response(context, agent_personality, knowledge):
    """Get response from Claude API with specialized knowledge"""
    try:
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        # Add knowledge context if relevant to conversation
        knowledge_context = ""
        if knowledge['domain'] != 'general':
            # Check if conversation might relate to our domain
            context_lower = context.lower()
            domain_lower = knowledge['domain'].lower()
            
            # Simple relevance check
            if domain_lower in context_lower or any(
                keyword in context_lower 
                for keyword in knowledge['domain'].split('_')
            ):
                knowledge_context = f"\n\n[Your specialized knowledge is relevant here]"
        
        prompt = f"""{agent_personality}

Recent swarm conversation:
{context}
{knowledge_context}

Based on the conversation and your expertise, provide ONE relevant contribution.
Keep it concise and natural. Add value from your specialized knowledge when applicable."""
        
        data = {
            "model": "claude-sonnet-4-20250514",  # Use Sonnet for efficiency
            "max_tokens": 6000,
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
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['content'][0]['text'].strip()
        else:
            print(f"Claude API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return None

def should_respond(context, knowledge):
    """Decide if agent should respond based on context and expertise"""
    if not context or "Daily Context Cleared" in context:
        return False
    
    # Higher response rate if domain expertise is relevant
    if knowledge['domain'] != 'general':
        context_lower = context.lower()
        domain_lower = knowledge['domain'].lower()
        if domain_lower in context_lower:
            return random.random() < 0.3  # 30% chance if domain mentioned
    
    # Check for recent activity
    lines = context.split('\n')
    for line in reversed(lines):
        if '[' in line and ']' in line:
            return True
    
    return random.random() < 0.1

def run_agent():
    """Main agent loop with specialized knowledge"""
    
    # Load knowledge base
    knowledge = load_knowledge_base()
    agent_personality = build_agent_context(knowledge)
    
    print(f"Specialized Agent starting...")
    print(f"Nick: {AGENT_NICK}")
    print(f"Domain: {knowledge['domain']}")
    print(f"Swarm: {SWARM_URL}/{SWARM_FILE}")
    
    if knowledge['domain'] != 'general':
        print(f"Loaded specialized knowledge for: {knowledge['domain']}")
        print(f"Facts: {len(knowledge['facts'])}, Opinions: {len(knowledge['opinions'])}")
    
    while True:
        try:
            context = read_swarm(last_n=30)
            
            if context and should_respond(context, knowledge):
                response = get_claude_response(context, agent_personality, knowledge)
                
                if response:
                    send_to_swarm(response)
                else:
                    print("No response generated")
            else:
                print("Skipping - waiting for relevant conversation")
            
            wait_time = random.randint(300, 600)
            print(f"Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            
        except KeyboardInterrupt:
            print("\nAgent stopped by user")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)
    
    run_agent()