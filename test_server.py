#!/usr/bin/env python3
"""Quick test to verify the server starts without errors."""

import sys
import subprocess
import time
import requests
from pathlib import Path

def test_server():
    # Change to project directory
    project_dir = Path(__file__).parent
    
    print(f"Testing server startup in: {project_dir}")
    
    # Start server in background
    try:
        proc = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "app.main:app", 
            "--host", "127.0.0.1", "--port", "8000"
        ], cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(5)
        
        # Test connection
        try:
            response = requests.get("http://127.0.0.1:8000/", timeout=5)
            if response.status_code == 200:
                print("✅ Server is running successfully!")
                print("🔗 Open: http://127.0.0.1:8000/")
                return True
            else:
                print(f"❌ Server returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection failed: {e}")
            return False
        finally:
            proc.terminate()
            proc.wait()
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)
