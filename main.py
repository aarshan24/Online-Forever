import os
import sys
import json
import time
import requests
import threading
import websocket
from keep_alive import keep_alive

status = "online"  # online/dnd/idle
custom_status = "discord.gg/permfruits"  # Custom status
token = os.getenv('TOKEN')

if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": token, "Content-Type": "application/json"}

def set_status(status, custom_status):
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.create_connection(ws_url)
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
    cstatus_payload = {
        "op": 3,
        "d": {
            "since": 0,
            "activities": [
                {
                    "type": 4,
                    "state": custom_status,
                    "name": "Custom Status",
                    "id": "custom",
                }
            ],
            "status": status,
            "afk": False,
        },
    }
    ws.send(json.dumps(cstatus_payload))

def check_dm():
    dm_channel_id = "1204989685852676106"  # Replace this with your actual DM channel ID
    dm_url = f"https://discord.com/api/v9/channels/{dm_channel_id}/messages?limit=1"
    dm_response = requests.get(dm_url, headers=headers)
    if dm_response.status_code == 200:
        dm_data = dm_response.json()
        if dm_data:
            last_message = dm_data[0]["content"]
            if "Welcome to Bloxtime Army" in last_message:
                print("Received 'Welcome to Bloxtime Army' message in DM. Changing status to 'discord.gg/permfruits'")
                set_status(status, custom_status)
            else:
                print("No 'Welcome to Bloxtime Army' message found in DM. Changing status to 'bro what'")
                set_status(status, "bro what")
        else:
            print("No messages found in DM.")
    else:
        print("Failed to fetch DM messages. Status code:", dm_response.status_code)

def on_message(ws, message):
    print("Received:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("WebSocket connection closed")

def on_open(ws):
    print("WebSocket connection opened")
    set_status(status, custom_status)

def onliner(token, status):
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

def run_onliner():
    while True:
        onliner(token, status)
        time.sleep(30)

keep_alive()
threading.Thread(target=run_onliner).start()
threading.Thread(target=check_dm).start()
