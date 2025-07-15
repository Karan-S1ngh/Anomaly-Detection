from ml_engine import process_behavior_session

# Define and test a session
session = {
    "typing_speed": 6.5,        # noticeably slower (~50 WPM instead of 84)
    "click_rate": 13,           # slightly more active clicking (maybe nervous)
    "mouse_speed": 9,           # a bit faster cursor movement
    "scroll_ratio": 0.9,        # scrolls slightly more than usual
    "login_hour": 15,           # same time
    "ip_country": "IN",         # same country
    "device_type": "Laptop"     # same device
}



result = process_behavior_session("karan", session)
print(result)
