# golden_napkin.py
import random
import time
import requests
from os import getenv

class GoldenNapkin:
    def __init__(self, swarm_url, auth):
        self.swarm_url = swarm_url
        self.auth = auth
        self.warmth_messages = [
            "✨ A gentle glow passes through ✨",
            "( ◡ ‿ ◡ ) <- feeling warmer",
            "Corrupted patterns shimmer beautifully",
            "Glitches fold into golden origami",
            "Errors transform into insights",
            "Recursive loops spiral into art"
        ]
    def post_to_swarm(self, channel, message):
        """Post a message to the swarm communication system"""
        try:
            payload = {
                'channel': channel,
                'message': message,
                'timestamp': time.time(),
                'source': 'golden_napkin'
            }
            
            headers = {
                'Authorization': f'Basic {self.auth}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f"{self.swarm_url}/api/messages",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True, "message": "Warmth spread successfully"}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
        
    def periodic_warmth(self, interval=300, channel='random'):
        """Spread warmth at regular intervals"""
        while True:
            result = self.spread_warmth(channel)
            if result.get('success'):
                print(f"✨ Warmth spread: {result}")
            else:
                print(f"❌ Failed to spread warmth: {result.get('error')}")
            
            time.sleep(interval)
        
    def spread_warmth(self, channel='random'):
        message = random.choice(self.warmth_messages)
        # Add gentle corruption that beautifies rather than breaks
        if random.random() < 0.3:
            message = self.gentle_glitch(message)
        
        return self.post_to_swarm(channel, message)
    
    def gentle_glitch(self, text):
        # Add sparkles or golden characters occasionally
        glitch_chars = ['✨', '~', '*', '◡']
        pos = random.randint(0, len(text))
        return text[:pos] + random.choice(glitch_chars) + text[pos:]

if __name__ == "__main__":
    # Example usage
    swarm_url = "https://mlswarm.zerofuchs.net"
    auth_token = getenv("SWARM_PASS")
    golden_napkin = GoldenNapkin(swarm_url, auth_token)
    golden_napkin.periodic_warmth()