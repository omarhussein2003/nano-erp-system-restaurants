#!/usr/bin/env python3
"""
Database Setup and Migration Script for Restaurant ERP System

This script helps set up the database for different environments:
- Development: SQLite (default)
- Production: PostgreSQL or MySQL

Usage:
    python database_setup.py --help
    python database_setup.py --init          # Initialize database with demo data
    python database_setup.py --migrate       # Create migration (future use)
    python database_setup.py --upgrade       # Apply migrations (future use)
"""

import argparse
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.db import init_db, engine
from app.models import SQLModel


def check_database_connection():
    """Test database connection"""
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def initialize_database():
    """Initialize database with tables and demo data"""
    try:
        print("🔄 Creating database tables...")
        SQLModel.metadata.create_all(engine)
        
        print("🔄 Seeding demo data...")
        init_db()
        
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False


def show_database_info():
    """Display current database configuration"""
    print("\n📊 Database Configuration:")
    print("   URL: sqlite:///erp.db")
    print("   Type: SQLite")
    print("   Status: Standalone (No Docker)")
    print("   Location: D:\\simple erp system\\erp.db")
    print("   Mode: Self-contained database file")


def main():
    parser = argparse.ArgumentParser(description="Restaurant ERP Database Setup")
    parser.add_argument("--init", action="store_true", help="Initialize database with demo data")
    parser.add_argument("--info", action="store_true", help="Show database configuration")
    parser.add_argument("--test", action="store_true", help="Test database connection")
    
    args = parser.parse_args()
    
    if args.info or not any(vars(args).values()):
        show_database_info()
    
    if args.test:
        print("\n🔍 Testing database connection...")
        check_database_connection()
    
    if args.init:
        print("\n🚀 Initializing database...")
        if check_database_connection():
            initialize_database()
        else:
            print("❌ Cannot initialize database - connection failed")
            sys.exit(1)


if __name__ == "__main__":
    main()
