import os
import json
import datetime
import pandas as pd
from features_config import features
from baseline_engine import detect_anomaly

BASELINE_FILE = "baselines/user_baselines.json"
SESSION_DIR = "data/user_sessions"

os.makedirs("baselines", exist_ok=True)
os.makedirs(SESSION_DIR, exist_ok=True)

def load_baselines():
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_baselines(baselines):
    with open(BASELINE_FILE, "w") as f:
        json.dump(baselines, f, indent=4)

def save_user_session(user_id, session_data, status=None):
    file_path = os.path.join(SESSION_DIR, f"{user_id}.csv")
    
    # Add label if provided
    if status:
        session_data["anomaly_label"] = "Anomaly" if "Anomaly" in status else "Normal"
    
    # Ensure timestamp is added
    session_data["timestamp"] = datetime.datetime.now()

    df = pd.DataFrame([session_data])

    if os.path.exists(file_path):
        df.to_csv(file_path, mode="a", header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

def handle_login_session(user_id, session_data):
    # Only expected features
    session_data = {k: session_data[k] for k in features if k in session_data}

    # Load baseline
    baselines = load_baselines()

    if user_id not in baselines:
        baselines[user_id] = session_data
        save_baselines(baselines)
        save_user_session(user_id, session_data, "First-time user")
        return "First-time user (baseline saved)", 0.0

    # Detect anomaly
    status, score = detect_anomaly(user_id, session_data, baselines)

    # Save session with label
    save_user_session(user_id, session_data, status)

    return status, score
