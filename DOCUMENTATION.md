# ChatterBox – Technical Documentation

## 1. Introduction

ChatterBox is a real-time messaging application built using FastAPI, WebSockets, SQLite, HTML, CSS, and JavaScript. The system enables private communication between users with additional features such as file sharing, message editing, typing indicators, profile management, and NLP-based content moderation.

This document explains the system architecture, database schema, core logic, and feature implementation details.

---

## 2. System Architecture

ChatterBox follows a client-server architecture:

Frontend:
- HTML (UI structure)
- CSS (Styling)
- JavaScript (WebSocket handling & dynamic updates)

Backend:
- FastAPI (API & WebSocket server)
- SQLite (Database)
- Uvicorn (ASGI server)

Communication:
- HTTP (Login, Registration, Message history)
- WebSocket (Real-time messaging, typing indicator, editing)

---

## 3. Core Features

### 3.1 Authentication
- Users register and log in.
- Token-based authentication is used.
- Token stored in localStorage.
- WebSocket connection validated using token.

### 3.2 Real-Time Messaging
- Implemented using FastAPI WebSocket endpoint (`/ws`).
- Messages stored in SQLite.
- Private messaging between users.
- Chat history fetched via REST endpoint.

### 3.3 Message Editing
- Only sender can edit message.
- `is_edited` column tracks edits.
- WebSocket sends update to receiver.
- Frontend updates message dynamically.

### 3.4 File Sharing
- Files uploaded via input field.
- Stored in `/static/uploads/`.
- `file_path` saved in messages table.
- Download link displayed in chat.

### 3.5 Typing Indicator
- When user types, frontend sends:
  {
    "type": "typing",
    "receiver_id": X
  }
- Receiver sees “User is typing...”
- Indicator disappears after timeout.

### 3.6 Profile Management
- Upload profile picture.
- Remove profile picture.
- Stored in static folder.
- Displayed in sidebar/chat header.

---

## 4. NLP-Based Content Moderation

### 4.1 Abuse Detection
- Regex-based keyword matching.
- Function: `contains_abuse(content)`

### 4.2 Violation Tracking
Each user has:
- violation_count
- is_temp_blocked
- block_until

### 4.3 Warning System
- 1st violation → Warning 1/3
- 2nd violation → Warning 2/3
- 3rd violation → Temporary block (10 minutes)

### 4.4 Temporary Blocking
- Block time stored in `block_until`
- Auto-unblocks after duration expires
- Blocked messages logged in `blocked_messages`

---

## 5. Database Schema

### 5.1 Users Table

| Column            | Type     | Description |
|------------------|----------|------------|
| id               | INTEGER  | Primary key |
| username         | TEXT     | Unique username |
| password         | TEXT     | Hashed password |
| violation_count  | INTEGER  | Abuse count |
| is_temp_blocked  | INTEGER  | 0 or 1 |
| block_until      | TEXT     | Block expiration time |

---

### 5.2 Messages Table

| Column      | Type     | Description |
|------------|----------|------------|
| id         | INTEGER  | Primary key |
| sender_id  | INTEGER  | Sender user ID |
| receiver_id| INTEGER  | Receiver user ID |
| content    | TEXT     | Message text |
| timestamp  | TEXT     | UTC timestamp |
| is_edited  | INTEGER  | 0 or 1 |
| file_path  | TEXT     | Uploaded file path |

---

### 5.3 Blocked Messages Table

| Column    | Type     | Description |
|----------|----------|------------|
| id       | INTEGER  | Primary key |
| user_id  | INTEGER  | Violating user |
| content  | TEXT     | Blocked message |
| timestamp| TEXT     | Time of violation |

---

## 6. WebSocket Message Types

### Private Message
{
  "type": "private_message",
  "receiver_id": X,
  "content": "Hello"
}

### Edit Message
{
  "type": "edit_message",
  "message_id": X,
  "new_content": "Updated text"
}

### Typing Indicator
{
  "type": "typing",
  "receiver_id": X
}

### Warning Response
{
  "type": "warning",
  "message": "Warning 1/3"
}

### Block Response
{
  "type": "blocked",
  "message": "You are temporarily blocked"
}

---

## 7. Project Structure

chatterbox/
│
├── main.py
├── database.py
├── chat.db
├── static/
│   ├── style.css
│   └── uploads/
├── templates/
│   ├── login.html
│   ├── register.html
│   └── chat.html
└── DOCUMENTATION.md

---

## 8. Security Considerations

- Token-based authentication
- WebSocket validation before connection
- Abuse filtering
- Temporary blocking mechanism
- Server-side validation before message storage

---

## 9. Future Enhancements

- Group chat
- Read receipts (single/double tick)
- Permanent ban system
- AI-based NLP moderation
- JWT authentication
- Database migrations
- Cloud deployment

---

## 10. Conclusion

ChatterBox is a real-time messaging platform demonstrating:

- WebSocket communication
- Database-driven chat persistence
- User management
- Content moderation
- Full-stack integration

The project showcases backend logic design, real-time systems, database handling, and frontend dynamic updates.