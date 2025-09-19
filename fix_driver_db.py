import sqlite3
import os

def fix_driver_assignment_table():
    db_path = 'erp.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if order_id column allows NULL
        cursor.execute("PRAGMA table_info('driverassignment')")
        columns = cursor.fetchall()
        
        print("Current DriverAssignment table structure:")
        for col in columns:
            print(f"  {col[1]} - {col[2]} - NOT NULL: {col[3]}")
        
        # Drop and recreate the table to allow NULL order_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS driverassignment_new (
                id INTEGER PRIMARY KEY,
                order_id INTEGER,
                driver_name TEXT,
                status TEXT DEFAULT 'queued',
                updated_at TEXT,
                FOREIGN KEY (order_id) REFERENCES "order" (id)
            )
        ''')
        
        # Copy existing data
        cursor.execute('''
            INSERT INTO driverassignment_new (id, order_id, driver_name, status, updated_at)
            SELECT id, order_id, driver_name, status, updated_at 
            FROM driverassignment
        ''')
        
        # Drop old table and rename new one
        cursor.execute('DROP TABLE driverassignment')
        cursor.execute('ALTER TABLE driverassignment_new RENAME TO driverassignment')
        
        conn.commit()
        print("✅ DriverAssignment table updated to allow NULL order_id")
        
        conn.close()
        print("✅ Database schema updated successfully")
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")

if __name__ == "__main__":
    fix_driver_assignment_table()
