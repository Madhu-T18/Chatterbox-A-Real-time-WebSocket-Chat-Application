from datetime import datetime
from database import get_connection

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}  # user_id: websocket

    async def connect(self, user_id, websocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print("Active connections:", list(self.active_connections.keys()))

        conn = get_connection()
        conn.execute("UPDATE users SET is_online=1 WHERE id=?", (user_id,))
        conn.commit()
        conn.close()

    def disconnect(self, user_id):
        self.active_connections.pop(user_id, None)
        print("After disconnect:", list(self.active_connections.keys()))

        conn = get_connection()
        conn.execute(
            "UPDATE users SET is_online=0, last_seen=? WHERE id=?",
            (datetime.utcnow().isoformat(), user_id)
        )
        conn.commit()
        conn.close()

    async def send_private(self, receiver_id, message: dict):
        print("Trying to send to:", receiver_id)

        if receiver_id in self.active_connections:
            await self.active_connections[receiver_id].send_json(message)
        else:
            print("Receiver not connected.")

