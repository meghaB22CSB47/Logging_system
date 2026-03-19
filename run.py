#!/usr/bin/env python3
"""
Startup Script
Run this from the project root directory
"""
import os
import sys

# Change to backend directory
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
os.chdir(backend_dir)
sys.path.insert(0, os.getcwd())

print("Starting Cryptographic Log Security System...")
print(f"Working directory: {os.getcwd()}")

# Import and run
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
