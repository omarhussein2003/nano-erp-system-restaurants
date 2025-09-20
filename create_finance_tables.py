#!/usr/bin/env python3
"""
Database migration script to create finance-related tables
"""

import sqlite3
import os

def create_finance_tables():
    """Create finance tables for transactions and accounts"""
    
    db_path = "erp.db"
    
    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create Account table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS account (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                account_type TEXT NOT NULL,
                balance REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Created account table")
        
        # Create Transaction table (using finance_transaction to avoid SQL keyword conflict)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS finance_transaction (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                reference TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES account (id)
            )
        """)
        print("✅ Created finance_transaction table")
        
        # Create default revenue account
        cursor.execute("""
            INSERT OR IGNORE INTO account (id, name, account_type, balance)
            VALUES (1, 'Sales Revenue', 'revenue', 0.0)
        """)
        print("✅ Created default revenue account")
        
        conn.commit()
        conn.close()
        
        print("✅ Finance tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating finance tables: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Creating finance tables...")
    success = create_finance_tables()
    if success:
        print("🎉 Finance tables ready! Orders will now create finance transactions.")
    else:
        print("💥 Failed to create finance tables. Please check the error messages above.")
