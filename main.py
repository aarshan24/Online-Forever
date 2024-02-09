import os
import sys
import json
import time
import requests
import threading
import websocket
from keep_alive import keep_alive
import queue

status = "online"  # online/dnd/idle
custom_status = "discord.gg/permfruits"  # Custom status

token = os.getenv('TOKEN')
if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": token, "Content-Type": "application/json"}

validate = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = validate.json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

# Create a queue for managing status update requests
status_queue = queue.Queue()

def on_message(ws, message):
    print("Received:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status, close_reason):
    print(f"WebSocket connection closed with status: {close_status} and reason: {close_reason}")


def on_open(ws):
    print("WebSocket connection opened")

    auth_payload = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows",
            },
            "presence": {"status": status, "afk": False},
        }
    }

    ws.send(json.dumps(auth_payload))

def update_status(ws):
    while True:
        # Get the next status update request from the queue
        status_payload = status_queue.get()
        
        # Send the status update payload
        ws.send(json.dumps(status_payload))
        
        # Put a delay between status updates (e.g., 59 seconds)
        time.sleep(59)

def onliner(token, status):
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)

    # Start a new thread to handle status updates
    threading.Thread(target=update_status, args=(ws,), daemon=True).start()

    ws.run_forever()

def run_onliner():
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    onliner(token, status)

keep_alive()
run_onliner()
