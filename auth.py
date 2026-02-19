import bcrypt
import secrets
from database import get_connection

def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes):
    return bcrypt.checkpw(password.encode(), hashed)

def create_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
    except:
        conn.close()
        return False

    conn.close()
    return True

def login_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if not user:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    token = secrets.token_hex(32)

    cursor.execute("UPDATE users SET token=? WHERE id=?",
                   (token, user["id"]))
    conn.commit()
    conn.close()

    return token

def get_user_by_token(token: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE token=?", (token,))
    user = cursor.fetchone()
    conn.close()

    return user

