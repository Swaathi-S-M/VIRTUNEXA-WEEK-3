import sqlite3

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM transactions")
conn.commit()
conn.close()

print("All transaction records deleted.")
