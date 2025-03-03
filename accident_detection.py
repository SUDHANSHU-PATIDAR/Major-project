import os
import cv2    
import geocoder
from geopy.geocoders import Nominatim
from datetime import datetime
from twilio.rest import Client

# Twilio credentials
account_sid = "AC0fe931584d037885efa617d4e98ec3c4"
auth_token = "1c50debfa2cad6427725b359370ffd48"
client = Client(account_sid, auth_token)

def detect_accident(video_path):
    cap = cv2.VideoCapture(video_path)
    count = 0
    accident_detected = False
    accident_details = ""
    vehicle_category = "Car"
    accident_type = "Collision"
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Placeholder accident detection logic
        if count % 50 == 0:
            accident_detected = True
            accident_details = f"Accident detected at frame {count}\n"
        
        count += 1
    
    cap.release()
    return accident_detected, accident_details, vehicle_category, accident_type

def save_accident_report(details, location, vehicle_category, accident_type):
    accident_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("Accident.txt", "w") as file:
        file.write(f"Accident Report\nDate: {accident_date}\nVehicle Category: {vehicle_category}\nAccident Type: {accident_type}\n{details}\nLocation: {location}\n")

def send_alert(location, vehicle_category, accident_type):
    accident_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_body = f"🚨 Accident detected!\nDate: {accident_date}\nVehicle: {vehicle_category}\nType: {accident_type}\nLocation: {location}. Check Accident.txt for details."
    client.messages.create(
        body=message_body,
        from_="18723269956",
        to="919981302302"
    )

def process_video(video_path):
    g = geocoder.ip('me')
    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse(g.latlng)

    accident_occurred, details, vehicle_category, accident_type = detect_accident(video_path)

    if accident_occurred:
        save_accident_report(details, locname.address, vehicle_category, accident_type)
        send_alert(locname.address, vehicle_category, accident_type)
        return f"🚨 Accident detected!\nDetails: {details}\nLocation: {locname.address}"
    else:
        return "✅ No accident detected."
