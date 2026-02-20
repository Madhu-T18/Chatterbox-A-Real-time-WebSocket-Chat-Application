💬 ChatterBox – Real-Time Private Chat Application
📌 Project Overview

ChatterBox is a real-time private chat web application built using:

FastAPI (Backend)

SQLite (Database)

WebSockets (Real-time messaging)

HTML, CSS, JavaScript (Frontend)

The application allows users to:

Register & Login

Send private real-time messages

Edit messages

Upload files

Upload profile pictures

Update "About" section

Change password

View online/offline status

See typing indicators

🚀 Features
🔐 Authentication

User registration

Secure login with token

Password hashing

Change password option

Logout support

💬 Chat System

Real-time private messaging using WebSockets

Message history loading

Edit sent messages

Timestamp tracking

Message storage in SQLite

📂 File Sharing

Upload files in private chat

Stored in static/files/

File message saved in database

🖼 Profile Management

Upload profile picture

Update "About" section

Profile image stored in static/uploads/

🟢 Online Status

Shows online/offline users

Tracks active WebSocket connections

✏ Typing Indicator

Shows when the other user is typing

🏗 Project Structure
chatterbox/
│
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── chat.db
│
├── static/
│   ├── login.html
│   ├── register.html
│   ├── chat.html
│   ├── login.css
│   ├── chat.css
│   ├── default.png
│   ├── uploads/
│   ├── files/
│
└── README.md

🛠 Installation & Setup
1️⃣ Clone the Project
git clone <your-repo-url>
cd chatterbox/backend

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install fastapi uvicorn python-multipart

4️⃣ Run the Server
uvicorn main:app --reload


Server runs at:

http://127.0.0.1:8000

🗄 Database

Database used: SQLite

File: chat.db

Tables:

users

messages

🔌 API Endpoints
Authentication
Method	Endpoint	Description
POST	/register	Register new user
POST	/login	Login user
POST	/change-password	Change password
Chat
Method	Endpoint	Description
GET	/users	Get all users
GET	/messages/{receiver_id}	Get private chat history
POST	/upload-file	Upload file in chat
Profile
Method	Endpoint	Description
POST	/upload-profile	Upload profile picture
POST	/update-about	Update about section
WebSocket
ws://127.0.0.1:8000/ws?token=<user_token>


Used for:

Real-time messages

Typing indicator

Edit messages

🔒 Security

Passwords are hashed

Token-based authentication

Users validated on every protected endpoint

📌 Future Improvements

Group chat support

Message delete feature

Read receipts

Dark mode

JWT authentication

Better UI animations

Cloud file storage

Production deployment

👨‍💻 Author

Developed as an internship-level real-time chat project.

📜 License

This project is for educational and learning purposes.