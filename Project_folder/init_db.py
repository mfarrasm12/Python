import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    name TEXT PRIMARY KEY,
    quantity INTEGER,
    borrowed INTEGER DEFAULT 0
)
""")

# 🔑 FIX: composite PRIMARY KEY
cursor.execute("""
CREATE TABLE IF NOT EXISTS borrowed (
    username TEXT,
    book TEXT,
    qty INTEGER,
    PRIMARY KEY (username, book)
)
""")

cursor.execute("""
INSERT OR IGNORE INTO users (username, password, role)
VALUES ('admin', '1234', 'admin')
""")

conn.commit()
conn.close()

print("Database initialized")
