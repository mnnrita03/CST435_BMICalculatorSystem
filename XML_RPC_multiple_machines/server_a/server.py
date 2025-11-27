# server_a/server.py
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sqlite3
import os
import time

DB_FILE = os.path.join(os.path.dirname(__file__), "bmi_data.db")

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bmi_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            weight REAL,
            height REAL,
            age INTEGER,
            bmi REAL,
            category TEXT,
            recommendation TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


# ---------- Business Logic ----------
def submit_user(name, weight, height, age):
    """Store user, call other servers (B, C, D), and save result."""

    try:
        # Connect to other XML-RPC servers
        b = ServerProxy("http://server_b:8001/", allow_none=True)
        c = ServerProxy("http://server_c:8002/", allow_none=True)
        d = ServerProxy("http://server_d:8003/", allow_none=True)

        # 1️⃣ Call Server B to calculate BMI
        bmi_res = b.calculate_bmi_value(weight, height)
        if not bmi_res["ok"]:
            return {"ok": False, "error": bmi_res["error"]}
        bmi = bmi_res["bmi"]

        # 2️⃣ Call Server C to categorize BMI
        category = c.categorize_bmi(bmi)

        # 3️⃣ Call Server D to get health recommendation
        recommendation = d.get_recommendation(category, age)

        # 4️⃣ Store everything in local DB
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO bmi_data (name, weight, height, age, bmi, category, recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, weight, height, age, bmi, category, recommendation))
        conn.commit()
        conn.close()

        # ✅ Return summary (like REST version)
        return {
            "ok": True,
            "bmi": bmi,
            "category": category,
            "recommendation": recommendation
        }

    except Exception as e:
        return {"ok": False, "error": str(e)}


# ---------- Utility ----------
def get_all_data():
    """Retrieve all records from the database (for debugging)."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name, weight, height, age, bmi, category, recommendation, timestamp FROM bmi_data")
    rows = cur.fetchall()
    conn.close()
    data = [
        {
            "id": r[0],
            "name": r[1],
            "weight": r[2],
            "height": r[3],
            "age": r[4],
            "bmi": r[5],
            "category": r[6],
            "recommendation": r[7],
            "timestamp": r[8]
        }
        for r in rows
    ]
    return data


# ---------- Main ----------
if __name__ == "__main__":
    init_db()
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True)
    server.register_function(submit_user, "submit_user")
    server.register_function(get_all_data, "get_all_data")

    print("[Server A] XML-RPC BMI pipeline server running on port 8000...")
    print("Waiting for requests...")
    server.serve_forever()
