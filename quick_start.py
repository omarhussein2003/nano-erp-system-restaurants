#!/usr/bin/env python3
"""Quick start script to get the ERP running with minimal dependencies."""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Install minimal dependencies directly
    print("Installing dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", "--upgrade", "pip"
    ], check=True)
    
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0", 
        "sqlmodel==0.0.14",
        "SQLAlchemy==1.4.53",
        "Jinja2>=3.1",
        "python-multipart>=0.0.9",
        "passlib[bcrypt]>=1.7",
        "pydantic==1.10.13"
    ], check=True)
    
    # Test imports
    print("Testing imports...")
    try:
        import app.models
        print("✓ Models OK")
        import app.main
        print("✓ App OK")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return 1
    
    # Start server
    print("Starting server on http://127.0.0.1:8000")
    subprocess.run([
        sys.executable, "-m", "uvicorn", "app.main:app", 
        "--reload", "--host", "127.0.0.1", "--port", "8000"
    ])

if __name__ == "__main__":
    sys.exit(main())
