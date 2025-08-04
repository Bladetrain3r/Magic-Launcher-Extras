#!/usr/bin/env python3
"""
MLChat - Minimal local LLM chat with file/paste support
Assumes OpenAI-compatible API running locally (no auth)
"""

import sys
import json
import base64
import os
from pathlib import Path

# Optional imports
try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

class MLChat:
    def __init__(self):
        # Simple config - URL and model only
        self.config = self.load_config()
        self.base_url = os.environ.get('MLCHAT_URL', self.config.get('base_url', 'http://localhost:1234/v1'))
        self.model = os.environ.get('MLCHAT_MODEL', self.config.get('model', 'local-model'))
        
    def load_config(self):
        """Load config from JSON file if exists"""
        config_file = Path.home() / '.config' / 'mlchat' / 'config.json'
        if config_file.exists():
            try:
                return json.loads(config_file.read_text())
            except:
                return {}
        return {}
    
    def send_to_ai(self, content, is_image=False, prompt=None):
        """Send content to AI and print response"""
        # Build message
        if is_image:
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt or "What's in this image?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{content}"}}
                ]
            }]
        else:
            # For text, combine prompt with content if both exist
            if prompt and content:
                full_content = f"{prompt}\n\n{content}"
            else:
                full_content = prompt or content
                
            messages = [{"role": "user", "content": full_content}]
        
        # Debug output
        if os.environ.get('MLCHAT_DEBUG'):
            print(f"Sending to {self.base_url}/chat/completions", file=sys.stderr)
            print(f"Model: {self.model}", file=sys.stderr)
            print(f"Message preview: {str(messages[0])[:200]}...", file=sys.stderr)
        
        # Make request - NO AUTH HEADERS!
        import requests
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Content-Type": "application/json"},
                json={"model": self.model, "stream": False, "messages": messages},
                timeout=180
            )
            
            if response.ok:
                data = response.json()
                # Handle different response formats
                if 'choices' in data and data['choices']:
                    print(data['choices'][0]['message']['content'])  # ONLY success goes to stdout
                elif 'error' in data:
                    print(f"API Error: {data['error']}", file=sys.stderr)  # Errors to stderr
                else:
                    print(f"Unexpected response format: {json.dumps(data, indent=2)}", file=sys.stderr)
            else:
                print(f"Error: {response.status_code}", file=sys.stderr)  # To stderr
                try:
                    error_data = response.json()
                    print(f"Response: {json.dumps(error_data, indent=2)}", file=sys.stderr)
                except:
                    print(f"Response: {response.text}", file=sys.stderr)
                    
        except requests.exceptions.ConnectionError:
            print(f"Failed to connect to {self.base_url}", file=sys.stderr)
            print("Check that your local LLM server is running", file=sys.stderr)
            sys.exit(1)  # Exit with error code
        except requests.exceptions.Timeout:
            print("Request timed out after 30 seconds", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Request failed: {e}", file=sys.stderr)
            sys.exit(1)
    
    def handle_file(self, filepath, prompt=None):
        """Handle file input with optional prompt"""
        path = Path(filepath)
        if not path.exists():
            print(f"File not found: {filepath}")
            return
        
        # Check if image
        if HAS_PIL and path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            # Handle image
            try:
                img = Image.open(path)
                # Convert to base64
                import io
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG')
                img_str = base64.b64encode(buffer.getvalue()).decode()
                self.send_to_ai(img_str, is_image=True, prompt=prompt)
            except Exception as e:
                print(f"Error processing image: {e}")
        else:
            # Handle text
            try:
                content = path.read_text()
                # If no prompt provided, ask AI to analyze the file
                if not prompt:
                    prompt = f"Please analyze this {path.suffix} file:"
                self.send_to_ai(content, prompt=prompt)
            except Exception as e:
                print(f"Error reading file: {e}")
    
    def handle_paste(self, prompt=None):
        """Handle clipboard paste with optional prompt"""
        if not HAS_CLIPBOARD:
            print("Install pyperclip for clipboard support: pip install pyperclip")
            return
        
        try:
            content = pyperclip.paste()
            if content:
                if not prompt:
                    prompt = "Please analyze this clipboard content:"
                self.send_to_ai(content, prompt=prompt)
            else:
                print("Clipboard is empty")
        except Exception as e:
            print(f"Clipboard error: {e}")
    
    def run(self):
        """Simple command loop"""
        print("MLChat - Local LLM Chat")
        print(f"Using: {self.base_url} with model {self.model}")
        print("Commands: /file <path> [prompt], /paste [prompt], /quit")
        
        while True:
            try:
                user_input = input("> ").strip()
                
                if user_input == '/quit':
                    break
                elif user_input.startswith('/file '):
                    # Parse file command - might have prompt after filename
                    parts = user_input[6:].strip().split(' ', 1)
                    filepath = parts[0]
                    prompt = parts[1] if len(parts) > 1 else None
                    self.handle_file(filepath, prompt)
                elif user_input.startswith('/paste'):
                    # Paste might have prompt too
                    prompt = user_input[6:].strip() if len(user_input) > 6 else None
                    self.handle_paste(prompt)
                elif user_input.startswith('/'):
                    print("Unknown command. Use /file, /paste, or /quit")
                else:
                    # Regular message
                    self.send_to_ai(user_input)
                    
            except KeyboardInterrupt:
                print("\nBye!")
                break
            except Exception as e:
                print(f"Error: {e}")

def show_help():
    """Show help message"""
    print("""MLChat - Local LLM Chat Client

Usage:
    mlchat                      Interactive mode
    mlchat -c "prompt"          Send prompt and exit
    mlchat --help               Show this help
    echo "prompt" | mlchat      Pipe mode

Commands (interactive mode):
    /file <path> [prompt]   Send file contents to LLM with optional prompt
    /paste [prompt]         Send clipboard contents to LLM with optional prompt
    /quit                   Exit

Configuration:
    Environment variables (override config file):
        MLCHAT_URL      API base URL (default: http://localhost:1234/v1)
        MLCHAT_MODEL    Model name (default: local-model)
        MLCHAT_DEBUG    Set to 1 to see request details
    
    Config file: ~/.config/mlchat/config.json
        {
            "base_url": "http://localhost:1234/v1",
            "model": "llama-2"
        }

Examples:
    # Default local setup
    mlchat

    # Different port
    export MLCHAT_URL="http://localhost:8080/v1"
    mlchat

    # One-shot query
    mlchat -c "What is 2+2?"
    
    # Pipe with prompt
    cat error.log | mlchat -c "What errors are shown?"
    
    # Interactive with prompts
    > /file script.py explain this code
    > /paste what is this?
""")

def main():
    # Help check
    if '--help' in sys.argv or '-h' in sys.argv:
        show_help()
        return
    
    # Quick arg parsing for one-shot mode
    if len(sys.argv) > 1 and sys.argv[1] == '-c':
        # Command mode - rest of args is the prompt
        if len(sys.argv) > 2:
            prompt = ' '.join(sys.argv[2:])
            # Check if stdin has data
            if not sys.stdin.isatty():
                content = sys.stdin.read().strip()
                if content:
                    chat = MLChat()
                    chat.send_to_ai(content, prompt=prompt)
                else:
                    # Just the prompt
                    chat = MLChat()
                    chat.send_to_ai(prompt)
            else:
                # Just the prompt, no piped input
                chat = MLChat()
                chat.send_to_ai(prompt)
        else:
            print("Error: -c requires a prompt")
    elif not sys.stdin.isatty():
        # Piped input without -c
        content = sys.stdin.read().strip()
        if content:
            chat = MLChat()
            # For piped content without prompt, ask for analysis
            chat.send_to_ai(content, prompt="Please analyze this input:")
        else:
            print("No input received")
    else:
        # Interactive mode
        chat = MLChat()
        chat.run()

if __name__ == "__main__":
    main()