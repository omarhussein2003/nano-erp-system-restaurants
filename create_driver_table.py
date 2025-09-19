import sqlite3
import os

def create_simple_driver_table():
    db_path = 'erp.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create a simple drivers table instead of using DriverAssignment
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drivers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.commit()
        print("✅ Simple drivers table created successfully")
        
        # Test insert
        cursor.execute("INSERT OR IGNORE INTO drivers (name) VALUES (?)", ("Test Driver",))
        conn.commit()
        
        # Check data
        cursor.execute("SELECT * FROM drivers")
        drivers = cursor.fetchall()
        print(f"Drivers in table: {drivers}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating table: {e}")

if __name__ == "__main__":
    create_simple_driver_table()
