from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from database import init_db, get_connection
from auth import create_user, login_user, get_user_by_token
from websocket_manager import ConnectionManager
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import UploadFile, File,Form
import sqlite3
import shutil
import os

os.makedirs("static/uploads", exist_ok=True)



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

manager = ConnectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# ------------------ AUTH ROUTES ------------------
class UserRequest(BaseModel):
    username: str
    password: str
@app.get("/")
def login_page():
    return FileResponse("static/login.html")


@app.get("/register-page")
def register_page():
    return FileResponse("static/register.html")


@app.get("/chat-page")
def chat_page():
    return FileResponse("static/chat.html")
@app.post("/register")
async def register(data: UserRequest):
    success = create_user(data.username, data.password)
    if not success:
        raise HTTPException(status_code=400, detail="User exists")
    return {"message": "User created"}
@app.post("/login")
async def login(data: UserRequest):
    token = login_user(data.username, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = get_user_by_token(token)

    return {
        "token": token,
        "user_id": user["id"]
    }




# ------------------ USERS LIST ------------------

@app.get("/users")

async def get_users():
    conn = get_connection()
    users = conn.execute("SELECT id, username, is_online, last_seen, profile_pic, about FROM users").fetchall()

    conn.close()
    return [dict(user) for user in users]

# ------------------ CHAT HISTORY ------------------

@app.get("/messages/{receiver_id}")
async def get_messages(receiver_id: int, token: str):

    user = get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    current_user_id = user["id"]  # 🔥 extract id correctly

    conn = sqlite3.connect("chat.db")
    conn.row_factory = sqlite3.Row

    messages = conn.execute("""
        SELECT * FROM messages
        WHERE (sender_id = ? AND receiver_id = ?)
           OR (sender_id = ? AND receiver_id = ?)
        ORDER BY timestamp
    """, (
        current_user_id, receiver_id,
        receiver_id, current_user_id
    )).fetchall()

    conn.close()

    return [dict(row) for row in messages]

@app.post("/change-password")
async def change_password(data: dict):
    token = data.get("token")
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    user = get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=401)

    from auth import verify_password, hash_password

    if not verify_password(old_password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Wrong old password")

    conn = get_connection()
    conn.execute(
        "UPDATE users SET password_hash=? WHERE id=?",
        (hash_password(new_password), user["id"])
    )
    conn.commit()
    conn.close()

    return {"message": "Password changed"}
@app.post("/upload-profile")
async def upload_profile(file: UploadFile = File(...), token: str = Form(...)):

    user = get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = user["id"]

    upload_folder = "static/uploads"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = f"{upload_folder}/{user_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    conn = sqlite3.connect("chat.db")
    conn.execute(
        "UPDATE users SET profile_pic = ? WHERE id = ?",
        (file_path, user_id)
    )
    conn.commit()
    conn.close()


    return {"message": "Profile updated", "path": file_path}

@app.post("/remove-profile")
async def remove_profile(token: str):
    user = get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=401)

    profile_path = user.get("profile_pic")

    # Remove file from folder
    if profile_path and os.path.exists(profile_path):
        os.remove(profile_path)

    conn = get_connection()
    conn.execute(
        "UPDATE users SET profile_pic=NULL WHERE id=?",
        (user["id"],)
    )
    conn.commit()
    conn.close()

    return {"message": "Profile removed"}

@app.post("/update-about")
async def update_about(data: dict):
    user = get_user_by_token(data.get("token"))
    if not user:
        raise HTTPException(status_code=401)

    conn = get_connection()
    conn.execute(
        "UPDATE users SET about=? WHERE id=?",
        (data.get("about"), user["id"])
    )
    conn.commit()
    conn.close()

    return {"message": "About updated"}


@app.post("/upload-file")
async def upload_file(token: str, receiver_id: int, file: UploadFile = File(...)):
    user = get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=401)

    os.makedirs("static/files", exist_ok=True)
    file_path = f"static/files/{user['id']}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    timestamp = datetime.utcnow().isoformat()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (sender_id, receiver_id, timestamp, file_path)
        VALUES (?, ?, ?, ?)
    """, (user["id"], receiver_id, timestamp, file_path))

    message_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "type": "private_message",
        "id": message_id,
        "sender_id": user["id"],
        "receiver_id": receiver_id,
        "file_path": file_path,
        "timestamp": timestamp
    }

# ------------------ WEBSOCKET ------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    token = websocket.query_params.get("token")
    user = get_user_by_token(token)

    if not user:
        await websocket.close()
        return

    user_id = user["id"]

    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            # ================= PRIVATE MESSAGE =================
            if data["type"] == "private_message":

                conn = get_connection()
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                # ---- Check temp block ----
                user_data = cursor.execute(
                    "SELECT violation_count, is_temp_blocked, block_until FROM users WHERE id=?",
                    (user_id,)
                ).fetchone()

                from datetime import datetime

                if user_data["is_temp_blocked"] == 1:
                    block_until = datetime.fromisoformat(user_data["block_until"])

                    if datetime.utcnow() < block_until:
                        await websocket.send_json({
                            "type": "blocked",
                            "message": "You are temporarily blocked for 10 minutes."
                        })
                        conn.close()
                        continue
                    else:
                        # Auto unblock
                        cursor.execute("""
                            UPDATE users
                            SET is_temp_blocked=0,
                                violation_count=0
                            WHERE id=?
                        """, (user_id,))
                        conn.commit()

                # ---- Check abuse ----
                from utils.moderation import contains_abuse, block_user_temporarily

                if contains_abuse(data["content"]):

                    # Log blocked message
                    cursor.execute("""
                        INSERT INTO blocked_messages (user_id, content, timestamp)
                        VALUES (?, ?, ?)
                    """, (user_id, data["content"], datetime.utcnow().isoformat()))

                    new_count = user_data["violation_count"] + 1

                    cursor.execute("""
                        UPDATE users
                        SET violation_count=?
                        WHERE id=?
                    """, (new_count, user_id))

                    conn.commit()

                    if new_count >= 3:
                        block_user_temporarily(conn, user_id)

                        await websocket.send_json({
                            "type": "blocked",
                            "message": "You are blocked for 10 minutes due to repeated violations."
                        })
                    else:
                        await websocket.send_json({
                            "type": "warning",
                            "message": f"Warning {new_count}/3: Inappropriate language detected."
                        })

                    conn.close()
                    continue

                # ---- Save normal message ----
                timestamp = datetime.utcnow().isoformat()

                cursor.execute("""
                    INSERT INTO messages (sender_id, receiver_id, content, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (user_id, data["receiver_id"], data["content"], timestamp))

                message_id = cursor.lastrowid
                conn.commit()
                conn.close()

                message_payload = {
                    "type": "private_message",
                    "id": message_id,
                    "sender_id": user_id,
                    "receiver_id": data["receiver_id"],
                    "content": data["content"],
                    "timestamp": timestamp,
                    "is_edited": 0
                }

                await manager.send_private(data["receiver_id"], message_payload)
                await websocket.send_json(message_payload)

            # ================= EDIT MESSAGE =================
            elif data["type"] == "edit_message":

                conn = sqlite3.connect("chat.db")
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                msg = cursor.execute(
                    "SELECT * FROM messages WHERE id=?",
                    (data["message_id"],)
                ).fetchone()

                if msg and msg["sender_id"] == user_id:

                    cursor.execute("""
                        UPDATE messages
                        SET content=?, is_edited=1
                        WHERE id=?
                    """, (data["new_content"], data["message_id"]))

                    conn.commit()

                    edit_payload = {
                        "type": "edit_message",
                        "message_id": data["message_id"],
                        "new_content": data["new_content"]
                    }

                    await manager.send_private(msg["receiver_id"], edit_payload)
                    await websocket.send_json(edit_payload)

                conn.close()

    except WebSocketDisconnect:
        manager.disconnect(user_id)

        
        