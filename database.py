import sqlite3

DB_NAME = "chat.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
   
    # MESSAGES TABLE (with status column added properly)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    content TEXT,
    timestamp TEXT,
    is_edited INTEGER DEFAULT 0,
    file_path TEXT
)
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT,
    token TEXT,
    is_online INTEGER DEFAULT 0,
    last_seen TEXT,
    profile_pic TEXT,
    about TEXT
)
    """)


    conn.commit()
    conn.close()
