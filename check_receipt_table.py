import sqlite3

# Check if ReceiptHistory table exists
conn = sqlite3.connect('erp.db')
cursor = conn.cursor()

# Check for receipthistory table
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='receipthistory'")
result = cursor.fetchone()
print(f"ReceiptHistory table exists: {bool(result)}")

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("\nAll tables in database:")
for table in tables:
    print(f"- {table[0]}")

# If receipthistory doesn't exist, create it
if not result:
    print("\nCreating ReceiptHistory table...")
    cursor.execute("""
        CREATE TABLE receipthistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            invoice_id INTEGER,
            receipt_number TEXT NOT NULL,
            receipt_content TEXT NOT NULL,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            generated_by INTEGER,
            print_count INTEGER DEFAULT 0,
            last_printed_at TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES "order" (id),
            FOREIGN KEY (invoice_id) REFERENCES invoice (id),
            FOREIGN KEY (generated_by) REFERENCES user (id)
        )
    """)
    conn.commit()
    print("✅ ReceiptHistory table created successfully!")

conn.close()
