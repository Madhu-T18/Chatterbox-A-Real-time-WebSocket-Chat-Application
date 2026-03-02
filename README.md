# 💬 Chatterbox  
### A Real-Time WebSocket Chat Application

Chatterbox is a real-time private messaging application built using FastAPI and WebSockets.  
It enables instant communication between users with message persistence, file sharing, and built-in content moderation.

---

## 🚀 Features

### 🔐 Authentication
- User Registration & Login
- Token-based WebSocket authentication
- Secure session validation

### 💬 Real-Time Messaging
- Private one-to-one chat
- Instant message delivery using WebSockets
- Persistent chat history using SQLite

### ✏️ Message Editing
- Edit sent messages
- Edited messages marked using `is_edited` flag
- Real-time update to receiver

### 📎 File Sharing
- Upload and send files
- Files stored on server
- Download links displayed in chat

### ⌨️ Typing Indicator
- Real-time typing notification
- Automatically hides after timeout

### 👤 Profile Management
- Upload profile picture
- Remove profile picture

### 🛡 Content Moderation (Basic NLP)
- Regex-based abusive word detection
- Violation counter per user
- 3-strike temporary blocking system
- Block duration tracking
- Blocked message logging

---

## 🧠 Moderation Logic

1. If abusive word detected → message blocked  
2. Violation count increases  
3. After 3 violations → temporary block  
4. Block time stored in database  
5. Blocked messages logged for audit  

---

## 🏗 Tech Stack

**Frontend**
- HTML
- CSS
- JavaScript

**Backend**
- FastAPI
- WebSockets
- SQLite
- Uvicorn

---

## 🗄 Database Schema

### Users
- id
- username
- password
- violation_count
- is_temp_blocked
- block_until

### Messages
- id
- sender_id
- receiver_id
- content
- timestamp
- is_edited
- file_path

### Blocked Messages
- id
- user_id
- content
- timestamp

---

## 📂 Project Structure
# 💬 Chatterbox  
### A Real-Time WebSocket Chat Application

Chatterbox is a real-time private messaging application built using FastAPI and WebSockets.  
It enables instant communication between users with message persistence, file sharing, and built-in content moderation.

---

## Features

### 🔐 Authentication
- User Registration & Login
- Token-based WebSocket authentication
- Secure session validation

### 💬 Real-Time Messaging
- Private one-to-one chat
- Instant message delivery using WebSockets
- Persistent chat history using SQLite

### ✏️ Message Editing
- Edit sent messages
- Edited messages marked using `is_edited` flag
- Real-time update to receiver

### 📎 File Sharing
- Upload and send files
- Files stored on server
- Download links displayed in chat

### ⌨️ Typing Indicator
- Real-time typing notification
- Automatically hides after timeout

### 👤 Profile Management
- Upload profile picture
- Remove profile picture

### 🛡 Content Moderation (Basic NLP)
- Regex-based abusive word detection
- Violation counter per user
- 3-strike temporary blocking system
- Block duration tracking
- Blocked message logging

---

## 🧠 Moderation Logic

1. If abusive word detected → message blocked  
2. Violation count increases  
3. After 3 violations → temporary block  
4. Block time stored in database  
5. Blocked messages logged for audit  

---

## 🏗 Tech Stack

**Frontend**
- HTML
- CSS
- JavaScript

**Backend**
- FastAPI
- WebSockets
- SQLite
- Uvicorn

---

## 🗄 Database Schema

### Users
- id
- username
- password
- violation_count
- is_temp_blocked
- block_until

### Messages
- id
- sender_id
- receiver_id
- content
- timestamp
- is_edited
- file_path

### Blocked Messages
- id
- user_id
- content
- timestamp

---
# 💬 Chatterbox  
### A Real-Time WebSocket Chat Application

Chatterbox is a real-time private messaging application built using FastAPI and WebSockets.  
It enables instant communication between users with message persistence, file sharing, and built-in content moderation.

---

## 🚀 Features

### 🔐 Authentication
- User Registration & Login
- Token-based WebSocket authentication
- Secure session validation

### 💬 Real-Time Messaging
- Private one-to-one chat
- Instant message delivery using WebSockets
- Persistent chat history using SQLite

### ✏️ Message Editing
- Edit sent messages
- Edited messages marked using `is_edited` flag
- Real-time update to receiver

### 📎 File Sharing
- Upload and send files
- Files stored on server
- Download links displayed in chat

### ⌨️ Typing Indicator
- Real-time typing notification
- Automatically hides after timeout

### 👤 Profile Management
- Upload profile picture
- Remove profile picture

### 🛡 Content Moderation (Basic NLP)
- Regex-based abusive word detection
- Violation counter per user
- 3-strike temporary blocking system
- Block duration tracking
- Blocked message logging

---

## 🧠 Moderation Logic

1. If abusive word detected → message blocked  
2. Violation count increases  
3. After 3 violations → temporary block  
4. Block time stored in database  
5. Blocked messages logged for audit  

---

## 🏗 Tech Stack

**Frontend**
- HTML
- CSS
- JavaScript

**Backend**
- FastAPI
- WebSockets
- SQLite
- Uvicorn

---

## 🗄 Database Schema

### Users
- id
- username
- password
- violation_count
- is_temp_blocked
- block_until

### Messages
- id
- sender_id
- receiver_id
- content
- timestamp
- is_edited
- file_path

### Blocked Messages
- id
- user_id
- content
- timestamp

---

## 📂 Project Structure
chatterbox/
│
├── main.py
├── database.py
├── chat.db
├── static/
│ ├── style.css
│ └── uploads/
├── templates/
│ ├── login.html
│ ├── register.html
│ └── chat.html
└── README.md
|__DOUCMENTATION


---

## ⚙️ Installation & Setup

1️⃣ Clone Repository
git clone https://github.com/Madhu-T18/Chatterbox-A-Real-time-WebSocket-Chat-Application.git
cd chatterbox
2️⃣ Install Dependencies
pip install fastapi uvicorn
3️⃣ Run Server
uvicorn main:app --reload
4️⃣ Open in Browser
http://127.0.0.1:8000

⚠️ Challenges Faced
WebSocket 403 authentication errors
SQLite threading issues
Duplicate table creation errors
WebSocket disconnect handling

🎯 Project Outcome
Chatterbox demonstrates:
Real-time WebSocket communication
Backend-driven moderation system
SQLite-based persistence
Full-stack integration

📄License
This project is developed for academic purposes.
