import os
import json
import time
import requests
import websocket
from threading import Thread

# Define the initial status and custom status
status = "online"
custom_status = "discord.gg/permfruits"
token = os.getenv('TOKEN')

def send_200_request():
    # Send a GET request to your external endpoint
    response = requests.get("https://disconline12345.onrender.com/")
    if response.status_code == 200:
        print("200 OK request received.")
        # Change the status to "bro what" for a second
        set_status("bro what")
        time.sleep(1)  # Wait for a second
        # Change the status to "discord.gg/permfruits"
        set_status("discord.gg/permfruits")
        return True
    else:
        print("Failed to receive 200 OK request.")
        return False

def set_status(new_custom_status):
    global status, custom_status
    # Update the custom status
    custom_status = new_custom_status
    # Implement the code to update the status via WebSocket connection or Discord API request
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
    payload = {
        "op": 3,
        "d": {
            "since": 0,
            "activities": [
                {
                    "type": 4,
                    "state": new_custom_status,
                    "name": "Custom Status",
                    "id": "custom",
                }
            ],
            "status": status,
            "afk": False,
        }
    }
    ws.send(json.dumps(payload))
    ws.close()

# This function continuously sends the 200 OK requests
def send_requests_continuously():
    while True:
        send_200_request()
        time.sleep(2)  # Wait for 2 minutes before sending the next request

# Run the function to continuously send requests in a separate thread
request_thread = Thread(target=send_requests_continuously)
request_thread.start()
