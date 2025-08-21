#!/usr/bin/env python3
"""
kv_auth.py - K/V JSON server with token-based authentication
No database needed - users ARE files
Under 200 lines of authenticated simplicity
"""

from flask import Flask, request, jsonify
import json
import hashlib
import secrets
from pathlib import Path
from functools import wraps
from datetime import datetime

# --- Configuration ---
app = Flask(__name__)
STORE_DIR = Path.home() / 'kv_store'
USERS_DIR = STORE_DIR / '_users'  # Underscore prefix to avoid collision
DATA_DIR = STORE_DIR / 'data'
PUBLIC_DIR = STORE_DIR / 'public'

# Create directories
for dir in [STORE_DIR, USERS_DIR, DATA_DIR, PUBLIC_DIR]:
    dir.mkdir(parents=True, exist_ok=True)

print(f"K/V store: {STORE_DIR}")
print(f"Users: {USERS_DIR}")
print(f"Protected data: {DATA_DIR}")
print(f"Public data: {PUBLIC_DIR}")

# --- Authentication Functions ---
def hash_token(token):
    """Hash a token for storage"""
    return hashlib.sha256(token.encode()).hexdigest()

def verify_auth():
    """Verify authentication from request headers"""
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return None, None
    
    try:
        # Format: "Bearer username:token"
        auth_parts = auth_header[7:].split(':', 1)
        if len(auth_parts) != 2:
            return None, None
            
        username, token = auth_parts
        
        # Check if user exists
        user_file = USERS_DIR / f"{username}.json"
        if not user_file.exists():
            return None, None
        
        # Verify token
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        if hash_token(token) == user_data['token_hash']:
            # Update last_seen
            user_data['last_seen'] = datetime.now().isoformat()
            with open(user_file, 'w') as f:
                json.dump(user_data, f, indent=2)
            return username, user_data
        
    except Exception as e:
        app.logger.error(f"Auth error: {e}")
    
    return None, None

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username, user_data = verify_auth()
        if username is None:
            return jsonify({"error": "Authentication required"}), 401
        request.username = username
        request.user_data = user_data
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username, user_data = verify_auth()
        if username is None:
            return jsonify({"error": "Authentication required"}), 401
        if not user_data.get('is_admin', False):
            return jsonify({"error": "Admin privileges required"}), 403
        request.username = username
        request.user_data = user_data
        return f(*args, **kwargs)
    return decorated_function

# --- Public Endpoints (No Auth) ---
@app.route('/public/<key>', methods=['GET'])
def get_public(key):
    """Get public data - no auth required"""
    file_path = PUBLIC_DIR / f"{key}.json"
    
    if not file_path.is_relative_to(PUBLIC_DIR):
        return jsonify({"error": "Invalid key"}), 400
    
    try:
        with open(file_path, 'r') as f:
            return f.read(), 200, {'Content-Type': 'application/json'}
    except FileNotFoundError:
        return jsonify({}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/public/<key>', methods=['POST'])
@require_auth
def set_public(key):
    """Set public data - requires auth to write"""
    file_path = PUBLIC_DIR / f"{key}.json"
    
    if not file_path.is_relative_to(PUBLIC_DIR):
        return jsonify({"error": "Invalid key"}), 400
    
    try:
        data = request.get_json()
        data['_modified_by'] = request.username
        data['_modified_at'] = datetime.now().isoformat()
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return jsonify({"status": "ok", "key": key}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Protected Endpoints (Auth Required) ---
@app.route('/kv/<key>', methods=['GET'])
@require_auth
def get_protected(key):
    """Get protected data - requires auth"""
    # User can only access their own data or shared data
    if '/' in key:
        owner, subkey = key.split('/', 1)
        if owner != request.username and not request.user_data.get('is_admin'):
            return jsonify({"error": "Access denied"}), 403
        file_path = DATA_DIR / owner / f"{subkey}.json"
    else:
        # Default to user's own namespace
        file_path = DATA_DIR / request.username / f"{key}.json"
    
    if not file_path.is_relative_to(DATA_DIR):
        return jsonify({"error": "Invalid key"}), 400
    
    try:
        with open(file_path, 'r') as f:
            return f.read(), 200, {'Content-Type': 'application/json'}
    except FileNotFoundError:
        return jsonify({}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/kv/<key>', methods=['POST'])
@require_auth
def set_protected(key):
    """Set protected data - requires auth"""
    # User can only write to their own namespace
    if '/' in key:
        owner, subkey = key.split('/', 1)
        if owner != request.username and not request.user_data.get('is_admin'):
            return jsonify({"error": "Access denied"}), 403
        file_path = DATA_DIR / owner / f"{subkey}.json"
    else:
        file_path = DATA_DIR / request.username / f"{key}.json"
    
    if not file_path.is_relative_to(DATA_DIR):
        return jsonify({"error": "Invalid key"}), 400
    
    # Ensure user directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        data = request.get_json()
        data['_modified_by'] = request.username
        data['_modified_at'] = datetime.now().isoformat()
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return jsonify({"status": "ok", "key": key}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- User Management (Admin Only) ---
@app.route('/users', methods=['GET'])
@require_admin
def list_users():
    """List all users - admin only"""
    users = []
    for user_file in USERS_DIR.glob("*.json"):
        with open(user_file, 'r') as f:
            user_data = json.load(f)
            # Don't send token hashes
            safe_data = {
                'username': user_file.stem,
                'created': user_data.get('created'),
                'last_seen': user_data.get('last_seen'),
                'is_admin': user_data.get('is_admin', False)
            }
            users.append(safe_data)
    
    return jsonify(users), 200

# --- Health Check ---
@app.route('/')
def index():
    """Basic info endpoint"""
    return jsonify({
        "service": "KV-Auth Server",
        "status": "running",
        "endpoints": {
            "public": "/public/<key> (GET: no auth, POST: auth required)",
            "protected": "/kv/<key> (auth required)",
            "users": "/users (admin only)"
        },
        "auth": "Use header: Authorization: Bearer username:token"
    }), 200

# --- Main ---
if __name__ == '__main__':
    print("\nKV-Auth Server")
    print("=" * 40)
    print("Public data: No auth for GET, auth for POST")
    print("Protected data: Auth required for all operations")
    print("Auth format: 'Authorization: Bearer username:token'")
    print("=" * 40)
    
    app.run(debug=True, port=5000, host='0.0.0.0')