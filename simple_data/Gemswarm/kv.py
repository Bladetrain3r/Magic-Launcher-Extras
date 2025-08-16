#!/usr/bin/env python3
# kv_server.py - A simple Key-Value JSON server for MLWebapps

# This is the entire backend. It's a Flask app that provides a minimal
# REST API for storing and retrieving JSON data by a key.
# It uses the filesystem as its database, storing each key as a separate
# JSON file.

from flask import Flask, request, jsonify, send_from_directory
import json
import os
from pathlib import Path

# --- Configuration ---
app = Flask(__name__)
# Define the directory where key-value data will be stored.
# This should be outside of the web server's document root for security.
STORE_DIR = Path.home() / 'kv_store'
STORE_DIR.mkdir(parents=True, exist_ok=True)
print(f"K/V store directory: {STORE_DIR}")

# --- API Endpoints ---
@app.route('/kv/<key>', methods=['GET'])
def get_key(key):
    """
    Retrieves the value for a given key.
    
    The key is the filename (e.g., 'team-a.json').
    If the file exists, it returns its content.
    If not, it returns a 404 with an empty JSON object.
    """
    file_path = STORE_DIR / f"{key}.json"
    
    # Check for path traversal vulnerabilities.
    if not file_path.is_relative_to(STORE_DIR):
        return jsonify({"error": "Invalid key"}), 400

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'application/json'}
    except FileNotFoundError:
        # Return an empty object for a non-existent key, which the frontend can handle.
        return jsonify({}), 404
    except Exception as e:
        app.logger.error(f"Error reading file for key '{key}': {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/kv/<key>', methods=['POST'])
def set_key(key):
    """
    Sets the value for a given key.
    
    The request body must be a valid JSON object.
    The JSON object is saved to a file named after the key.
    This overwrites any existing data for that key.
    """
    file_path = STORE_DIR / f"{key}.json"
    
    # Check for path traversal vulnerabilities.
    if not file_path.is_relative_to(STORE_DIR):
        return jsonify({"error": "Invalid key"}), 400

    # Ensure the incoming data is JSON.
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    try:
        data = request.get_json()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        return jsonify({"status": "ok", "message": f"Data for '{key}' saved successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error writing file for key '{key}': {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/')
def serve_index():
    """
    Serves the main index file.
    """
    return "The K/V-JSON backend is running. Please open your MLWebapp in a browser."

# --- Main Entry Point ---
if __name__ == '__main__':
    # Running in debug mode is fine for a development tool.
    app.run(debug=True, port=5000, host='0.0.0.0')

