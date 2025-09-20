#!/usr/bin/env python3
"""
Database migration script to add missing columns to the order table
"""

import sqlite3
import os

def fix_order_table():
    """Add missing columns to the order table"""
    
    db_path = "erp.db"
    
    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table_number column exists
        cursor.execute("PRAGMA table_info('order')")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"Current columns in order table: {columns}")
        
        # Add missing columns if they don't exist
        missing_columns = []
        
        if 'table_number' not in columns:
            missing_columns.append(('table_number', 'TEXT'))
        
        if 'payment_method' not in columns:
            missing_columns.append(('payment_method', 'TEXT'))
            
        if 'driver_name' not in columns:
            missing_columns.append(('driver_name', 'TEXT'))
            
        if 'sub_total' not in columns:
            missing_columns.append(('sub_total', 'REAL DEFAULT 0.0'))
            
        if 'tax_total' not in columns:
            missing_columns.append(('tax_total', 'REAL DEFAULT 0.0'))
            
        if 'grand_total' not in columns:
            missing_columns.append(('grand_total', 'REAL DEFAULT 0.0'))
        
        # Add missing columns
        for column_name, column_type in missing_columns:
            try:
                cursor.execute(f"ALTER TABLE 'order' ADD COLUMN {column_name} {column_type}")
                print(f"✅ Added column: {column_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"⚠️ Column {column_name} already exists")
                else:
                    print(f"❌ Error adding column {column_name}: {e}")
        
        conn.commit()
        
        # Verify the changes
        cursor.execute("PRAGMA table_info('order')")
        updated_columns = [column[1] for column in cursor.fetchall()]
        print(f"Updated columns in order table: {updated_columns}")
        
        conn.close()
        print("✅ Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing order table: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing order table schema...")
    success = fix_order_table()
    if success:
        print("🎉 Order table fixed! You can now create orders successfully.")
    else:
        print("💥 Failed to fix order table. Please check the error messages above.")
