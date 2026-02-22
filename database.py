import sqlite3
DB_NAME="chat.db"
def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        violation_count INTEGER DEFAULT 0,
        is_temp_blocked INTEGER DEFAULT 0,
        block_until TEXT
    )
    """)

    # MESSAGES TABLE
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

    # BLOCKED MESSAGES TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blocked_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        content TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()