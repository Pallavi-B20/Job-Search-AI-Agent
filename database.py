import sqlite3

def connect_db():
    return sqlite3.connect("jobs.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        salary TEXT,
        link TEXT
    )
    """)

    conn.commit()
    conn.close()