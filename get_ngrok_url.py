#!/usr/bin/env python3
"""
Script to automatically get the current ngrok URL and update .env
"""
import requests
import os
import re
from pathlib import Path

def get_ngrok_url():
    """Get the current ngrok public URL"""
    try:
        # ngrok exposes a local API at http://127.0.0.1:4040
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        data = response.json()
        
        for tunnel in data.get("tunnels", []):
            if tunnel.get("proto") == "https":
                return tunnel.get("public_url")
        
        print("No HTTPS tunnel found")
        return None
        
    except Exception as e:
        print(f"Error getting ngrok URL: {e}")
        return None

def update_env_file(ngrok_url):
    """Update the .env file with the new ngrok URL"""
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        print("No .env file found")
        return False
    
    # Read current content
    content = env_file.read_text()
    
    # Replace BASE_URL
    new_content = re.sub(
        r'BASE_URL=.*',
        f'BASE_URL={ngrok_url}',
        content
    )
    
    # Write back
    env_file.write_text(new_content)
    print(f"✅ Updated .env with: {ngrok_url}")
    return True

def main():
    """Main function"""
    print("🔗 Getting current ngrok URL...")
    
    ngrok_url = get_ngrok_url()
    if not ngrok_url:
        print("❌ Could not get ngrok URL. Make sure ngrok is running.")
        return
    
    print(f"📡 Found ngrok URL: {ngrok_url}")
    
    if update_env_file(ngrok_url):
        print("✅ .env file updated successfully!")
        print("🔄 Restart your backend server to use the new URL")
    else:
        print("❌ Failed to update .env file")

if __name__ == "__main__":
    main()