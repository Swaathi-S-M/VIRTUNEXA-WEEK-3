import sqlite3

def connect_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

def add_transaction(conn, trans_type, category, amount, date):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)",
        (trans_type, category, amount, date)
    )
    conn.commit()

def fetch_all_transactions(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    return cursor.fetchall()
