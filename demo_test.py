from ml_engine import process_behavior_session

# Define and test a session
session = {
    "typing_speed": 6,         
    "click_rate": 10,          
    "mouse_speed": 7,         
    "scroll_ratio": 0.8,       
    "ip_country": "IN",       
    "device_type": "Laptop"   
}

result = process_behavior_session("karan", session)
print(result)
