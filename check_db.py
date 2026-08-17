import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(leetcode_profiles)")
print(cursor.fetchall())

conn.close()