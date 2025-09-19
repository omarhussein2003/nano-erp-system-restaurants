import sqlite3
import os

def fix_database():
    db_path = 'erp.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if order_no column exists
        cursor.execute("PRAGMA table_info('order')")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'order_no' not in columns:
            print("Adding order_no column...")
            cursor.execute('ALTER TABLE "order" ADD COLUMN order_no TEXT')
            conn.commit()
            print("✅ Added order_no column")
        else:
            print("✅ order_no column already exists")
        
        conn.close()
        print("✅ Database schema updated successfully")
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")

if __name__ == "__main__":
    fix_database()
