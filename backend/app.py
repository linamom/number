import os
import requests
import psycopg2
import time
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

def get_db_connection():
    # Retry mechanism for database connection
    retries = 10
    while retries > 0:
        try:
            return psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
        except Exception as e:
            print(f"Waiting for database... ({retries} attempts left)")
            retries -= 1
            time.sleep(3)
    raise Exception("Could not connect to the database.")

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tb_number_save (
                id SERIAL PRIMARY KEY,
                first_num INTEGER,
                saved_num INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

counter_state = {
    "value": 0,
    "first_num": 0
}

@app.route("/api/counter", methods=["GET"])
def get_counter():
    return jsonify(counter_state)

@app.route("/api/counter/increment", methods=["POST"])
def increment():
    counter_state["value"] += 1
    return jsonify(counter_state)

@app.route("/api/counter/decrement", methods=["POST"])
def decrement():
    counter_state["value"] -= 1
    return jsonify(counter_state)

@app.route("/api/counter/reset", methods=["POST"])
def reset():
    counter_state["value"] = 0
    counter_state["first_num"] = 0
    return jsonify(counter_state)

@app.route("/api/counter/save", methods=["POST"])
def save():
    current_first = counter_state["first_num"]
    current_value = counter_state["value"]
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tb_number_save (first_num, saved_num) VALUES (%s, %s)",
            (current_first, current_value)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        counter_state["first_num"] = current_value
        
        return jsonify({
            "success": True, 
            "message": "Saved to local PostgreSQL!",
            "value": current_value,
            "first_num": current_value
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
