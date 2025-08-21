#!/usr/bin/env python3
"""
kv_client_example.py - Example client for KV-Auth Server
Shows how to use the authenticated K/V store
"""

import requests
import json
import sys

class KVClient:
    """Simple client for KV-Auth Server"""
    
    def __init__(self, base_url='http://localhost:5000', username=None, token=None):
        self.base_url = base_url
        self.username = username
        self.token = token
        self.session = requests.Session()
        
        # Set auth header if credentials provided
        if username and token:
            self.session.headers['Authorization'] = f'Bearer {username}:{token}'
    
    def get_public(self, key):
        """Get public data (no auth required)"""
        response = self.session.get(f'{self.base_url}/public/{key}')
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        return response.json()
    
    def set_public(self, key, data):
        """Set public data (requires auth)"""
        response = self.session.post(
            f'{self.base_url}/public/{key}',
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def get(self, key):
        """Get protected data (requires auth)"""
        response = self.session.get(f'{self.base_url}/kv/{key}')
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        return response.json()
    
    def set(self, key, data):
        """Set protected data (requires auth)"""
        response = self.session.post(
            f'{self.base_url}/kv/{key}',
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def list_users(self):
        """List all users (admin only)"""
        response = self.session.get(f'{self.base_url}/users')
        response.raise_for_status()
        return response.json()

def demo():
    """Demo the client functionality"""
    
    print("KV-Auth Client Demo")
    print("=" * 40)
    
    # Get credentials
    username = input("Username: ").strip()
    token = input("Token: ").strip()
    
    if not username or not token:
        print("Credentials required for most operations")
        return
    
    # Create client
    client = KVClient(username=username, token=token)
    
    while True:
        print("\nOptions:")
        print("1. Get public data")
        print("2. Set public data")
        print("3. Get your data")
        print("4. Set your data")
        print("5. List users (admin only)")
        print("6. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            key = input("Key: ").strip()
            data = client.get_public(key)
            print(f"Data: {json.dumps(data, indent=2)}")
        
        elif choice == '2':
            key = input("Key: ").strip()
            value = input("Value (JSON): ").strip()
            try:
                data = json.loads(value) if value else {}
            except json.JSONDecodeError:
                # If not valid JSON, treat as string
                data = {"value": value}
            result = client.set_public(key, data)
            print(f"Result: {result}")
        
        elif choice == '3':
            key = input("Key: ").strip()
            data = client.get(key)
            print(f"Data: {json.dumps(data, indent=2)}")
        
        elif choice == '4':
            key = input("Key: ").strip()
            value = input("Value (JSON): ").strip()
            try:
                data = json.loads(value) if value else {}
            except json.JSONDecodeError:
                data = {"value": value}
            result = client.set(key, data)
            print(f"Result: {result}")
        
        elif choice == '5':
            try:
                users = client.list_users()
                print("\nUsers:")
                for user in users:
                    admin = " [ADMIN]" if user.get('is_admin') else ""
                    print(f"  - {user['username']}{admin}")
            except requests.HTTPError as e:
                print(f"Error: {e}")
        
        elif choice == '6':
            break
        
        else:
            print("Invalid choice")

# Example: Using as a library
def example_usage():
    """Example of using the client programmatically"""
    
    # Initialize client with credentials
    client = KVClient(
        base_url='http://localhost:5000',
        username='alice',
        token='your-token-here'
    )
    
    # Store some data
    client.set('preferences', {
        'theme': 'dark',
        'notifications': True,
        'language': 'en'
    })
    
    # Retrieve data
    prefs = client.get('preferences')
    print(f"User preferences: {prefs}")
    
    # Store public data (readable by anyone)
    client.set_public('announcement', {
        'message': 'System maintenance at 2 AM',
        'date': '2025-01-20'
    })
    
    # Get public data (no auth needed)
    public_client = KVClient()  # No credentials
    announcement = public_client.get_public('announcement')
    print(f"Public announcement: {announcement}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'example':
        example_usage()
    else:
        demo()