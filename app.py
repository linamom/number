import os
import requests
from datetime import datetime
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Local initial state tracking
counter_state = {
    "value": 0,
    "first_num": 0  # Initial value when session started or reset
}

@app.route("/")
def index():
    return render_template("index.html")

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
    # When resetting, you might want to update first_num or keep it.
    # Here we reset both as it's a "fresh start".
    counter_state["value"] = 0
    counter_state["first_num"] = 0
    return jsonify(counter_state)

@app.route("/api/counter/save", methods=["POST"])
def save_to_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return jsonify({"success": False, "message": "Supabase credentials missing"}), 500
    
    # REST API headers (removed upsert prefer)
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    
    # 1. Target table name 'tb_number_save'
    url = f"{SUPABASE_URL}/rest/v1/tb_number_save"
    
    # 2. Payload for INSERT
    current_first = counter_state["first_num"]
    current_value = counter_state["value"]
    
    payload = {
        "first_num": current_first,
        "saved_num": current_value,
        "created_at": datetime.now().isoformat()
    }
    
    try:
        # Performing POST (Insert)
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            # CRITICAL: After successful save, set current value as the new first_num
            counter_state["first_num"] = current_value
            
            return jsonify({
                "success": True, 
                "message": f"Successfully inserted row! Next start from {current_value}",
                "value": current_value,
                "first_num": current_value
            })
        else:
            return jsonify({"success": False, "message": f"DB Error: {response.text}"}), response.status_code
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

if __name__ == "__main__":
    # In Docker, we must listen on 0.0.0.0 so the port mapping works
    app.run(debug=True, host="0.0.0.0", port=5000)
