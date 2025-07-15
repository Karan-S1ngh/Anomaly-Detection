# ml_engine.py

import os
from session_handler import handle_login_session

def process_behavior_session(user_id, session_data):
    """
    Process incoming session data for a user and return anomaly detection result.
    
    Args:
        user_id (str): Unique user identifier.
        session_data (dict): Dictionary of features for the current session.
    
    Returns:
        dict: {
            "status": "✅ Normal" or "❌ Anomaly",
            "score": float (0 to 1),
            "action": str (e.g., "Allow", "Trigger Re-Verification")
        }
    """
    status, score = handle_login_session(user_id, session_data)
    
    # Decide action based on anomaly score
    if status == "❌ Anomaly":
        action = "Trigger Re-Verification"
    else:
        action = "Allow"
    
    return {
        "status": status,
        "score": round(score, 3),
        "action": action
    }
