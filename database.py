import sqlite3


def init_db():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leetcode_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT UNIQUE,
            leetcode_username TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_leetcode_username(email, username):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO leetcode_profiles
        (user_email, leetcode_username)
        VALUES (?, ?)
    """, (email, username))

    conn.commit()
    conn.close()


def get_leetcode_username(email):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT leetcode_username
        FROM leetcode_profiles
        WHERE user_email = ?
    """, (email,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None