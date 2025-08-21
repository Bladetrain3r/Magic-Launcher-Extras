#!/usr/bin/env python3
"""
kv_auth_manager.py - Manage users for KV-Auth Server
Separate tool for security - no user creation in main service
Under 150 lines of user management
"""

import json
import hashlib
import secrets
import sys
import getpass
from pathlib import Path
from datetime import datetime

# Configuration - must match kv_auth.py
STORE_DIR = Path.home() / 'kv_store'
USERS_DIR = STORE_DIR / '_users'
DATA_DIR = STORE_DIR / 'data'

# Ensure directories exist
USERS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

def hash_token(token):
    """Hash a token for storage"""
    return hashlib.sha256(token.encode()).hexdigest()

def generate_token():
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

def add_user(username, token=None, is_admin=False):
    """Add a new user"""
    user_file = USERS_DIR / f"{username}.json"
    
    if user_file.exists():
        print(f"Error: User '{username}' already exists")
        return False
    
    # Generate token if not provided
    if token is None:
        token = generate_token()
        print(f"Generated token: {token}")
    
    # Create user data
    user_data = {
        'username': username,
        'token_hash': hash_token(token),
        'created': datetime.now().isoformat(),
        'last_seen': None,
        'is_admin': is_admin
    }
    
    # Save user file
    with open(user_file, 'w') as f:
        json.dump(user_data, f, indent=2)
    
    # Create user's data directory
    user_data_dir = DATA_DIR / username
    user_data_dir.mkdir(exist_ok=True)
    
    print(f"✓ User '{username}' created")
    if is_admin:
        print("  (with admin privileges)")
    
    return token

def remove_user(username):
    """Remove a user"""
    user_file = USERS_DIR / f"{username}.json"
    
    if not user_file.exists():
        print(f"Error: User '{username}' not found")
        return False
    
    # Confirm deletion
    confirm = input(f"Delete user '{username}' and all their data? (y/N): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return False
    
    # Remove user file
    user_file.unlink()
    
    # Optionally remove user's data
    user_data_dir = DATA_DIR / username
    if user_data_dir.exists():
        remove_data = input(f"Also delete user's data directory? (y/N): ")
        if remove_data.lower() == 'y':
            import shutil
            shutil.rmtree(user_data_dir)
            print(f"  Data directory removed")
    
    print(f"✓ User '{username}' removed")
    return True

def reset_token(username):
    """Reset a user's token"""
    user_file = USERS_DIR / f"{username}.json"
    
    if not user_file.exists():
        print(f"Error: User '{username}' not found")
        return None
    
    # Generate new token
    new_token = generate_token()
    
    # Update user file
    with open(user_file, 'r') as f:
        user_data = json.load(f)
    
    user_data['token_hash'] = hash_token(new_token)
    user_data['token_reset'] = datetime.now().isoformat()
    
    with open(user_file, 'w') as f:
        json.dump(user_data, f, indent=2)
    
    print(f"✓ Token reset for '{username}'")
    print(f"New token: {new_token}")
    return new_token

def list_users():
    """List all users"""
    users = list(USERS_DIR.glob("*.json"))
    
    if not users:
        print("No users found")
        return
    
    print(f"\nUsers ({len(users)}):")
    print("-" * 60)
    
    for user_file in sorted(users):
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        username = user_file.stem
        created = user_data.get('created', 'Unknown')[:10]
        last_seen = user_data.get('last_seen', 'Never')
        if last_seen != 'Never':
            last_seen = last_seen[:19]
        
        admin = " [ADMIN]" if user_data.get('is_admin') else ""
        
        print(f"  {username:<20} Created: {created}  Last seen: {last_seen}{admin}")
    
    print("-" * 60)

def toggle_admin(username):
    """Toggle admin status for a user"""
    user_file = USERS_DIR / f"{username}.json"
    
    if not user_file.exists():
        print(f"Error: User '{username}' not found")
        return False
    
    with open(user_file, 'r') as f:
        user_data = json.load(f)
    
    # Toggle admin status
    user_data['is_admin'] = not user_data.get('is_admin', False)
    
    with open(user_file, 'w') as f:
        json.dump(user_data, f, indent=2)
    
    status = "granted" if user_data['is_admin'] else "revoked"
    print(f"✓ Admin privileges {status} for '{username}'")
    return True

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("KV-Auth User Manager")
        print("=" * 40)
        print("\nUsage:")
        print("  kv_auth_manager.py add <username> [--admin]")
        print("  kv_auth_manager.py remove <username>")
        print("  kv_auth_manager.py reset <username>")
        print("  kv_auth_manager.py list")
        print("  kv_auth_manager.py admin <username>")
        print("\nExamples:")
        print("  kv_auth_manager.py add alice --admin")
        print("  kv_auth_manager.py reset bob")
        print("  kv_auth_manager.py list")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'add':
        if len(sys.argv) < 3:
            print("Error: Username required")
            sys.exit(1)
        
        username = sys.argv[2]
        is_admin = '--admin' in sys.argv
        
        # Optional: prompt for custom token
        custom = input("Enter custom token (or press Enter to generate): ").strip()
        token = custom if custom else None
        
        add_user(username, token, is_admin)
    
    elif command == 'remove':
        if len(sys.argv) < 3:
            print("Error: Username required")
            sys.exit(1)
        remove_user(sys.argv[2])
    
    elif command == 'reset':
        if len(sys.argv) < 3:
            print("Error: Username required")
            sys.exit(1)
        reset_token(sys.argv[2])
    
    elif command == 'list':
        list_users()
    
    elif command == 'admin':
        if len(sys.argv) < 3:
            print("Error: Username required")
            sys.exit(1)
        toggle_admin(sys.argv[2])
    
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)

if __name__ == '__main__':
    main()