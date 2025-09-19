import sqlite3
import requests
import json

def check_database():
    print("=== DATABASE CHECK ===")
    try:
        conn = sqlite3.connect('erp.db')
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='driverassignment'")
        table_exists = cursor.fetchone() is not None
        print(f"DriverAssignment table exists: {table_exists}")
        
        if table_exists:
            # Check table structure
            cursor.execute("PRAGMA table_info('driverassignment')")
            columns = cursor.fetchall()
            print("Table structure:")
            for col in columns:
                print(f"  {col[1]} - {col[2]} - NOT NULL: {col[3]}")
            
            # Check existing data
            cursor.execute("SELECT COUNT(*) FROM driverassignment")
            count = cursor.fetchone()[0]
            print(f"Existing records: {count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM driverassignment LIMIT 3")
                records = cursor.fetchall()
                print("Sample records:")
                for record in records:
                    print(f"  {record}")
        
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

def test_api():
    print("\n=== API TEST ===")
    try:
        # Test adding a driver
        url = "http://127.0.0.1:8000/delivery/api/drivers"
        data = {"name": "Test Driver"}
        
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code != 200:
            print("API call failed!")
        else:
            print("API call successful!")
            
    except Exception as e:
        print(f"API error: {e}")

if __name__ == "__main__":
    check_database()
    test_api()
