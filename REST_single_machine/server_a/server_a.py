from flask import Flask, request, jsonify
import requests, sqlite3

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute('''
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

init_db()

@app.route('/submit', methods=['POST'])
def handle_client_data():
    data = request.get_json()
    name = data.get("name")
    weight = data.get("weight")
    height = data.get("height")
    age = data.get("age")

    try:
        # --- Call Server B (BMI Calculation) ---
        b_response = requests.post("http://localhost:5001/calculate_bmi", json={"weight": weight, "height": height}, timeout=5)
        b_response.raise_for_status()
        bmi = b_response.json().get("bmi")

        # --- Call Server C (Category Classification) ---
        c_response = requests.post("http://localhost:5002/bmi_category", json={"bmi": bmi}, timeout=5)
        c_response.raise_for_status()
        category = c_response.json().get("category")

        # --- Call Server D (Health Recommendation) ---
        d_response = requests.post("http://localhost:5003/recommendation", json={"category": category, "age": age}, timeout=5)
        d_response.raise_for_status()
        recommendation = d_response.json().get("recommendation")

        # --- Store in SQLite ---
        conn = sqlite3.connect("bmi_data.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bmi_data (name, weight, height, age, bmi, category, recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, weight, height, age, bmi, category, recommendation))
        conn.commit()
        conn.close()

        # ✅ Return flat structure for client.py
        return jsonify({
            "bmi": bmi,
            "category": category,
            "recommendation": recommendation
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Service communication failed: {e}"}), 500

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
