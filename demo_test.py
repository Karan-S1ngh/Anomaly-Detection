from ml_engine import process_behavior_session

# Define and test a session
session = {
    "typing_speed": 6.5,        
    "click_rate": 13,           
    "mouse_speed": 9,           
    "scroll_ratio": 0.9,        
    "login_hour": 15,           
    "ip_country": "IN",         
    "device_type": "Laptop"     
}



result = process_behavior_session("karan", session)
print(result)
