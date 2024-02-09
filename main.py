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
alternate_status = "bro what"

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

def on_message(ws, message):
    print("Received:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("WebSocket connection closed unexpectedly. Reconnecting...")
    # Exponential backoff and retry logic
    retry_delay = 1
    while True:
        time.sleep(retry_delay)
        print("Attempting to reconnect...")
        try:
            onliner(token, status)
            print("Reconnection successful")
            return
        except Exception as e:
            print(f"Reconnection failed: {e}")
            # Increase retry delay exponentially
            retry_delay *= 2
            if retry_delay > 60:
                retry_delay = 60  # Cap maximum retry delay at 60 seconds

def on_open(ws):
    print("WebSocket connection opened")

    def update_status():
        while True:
            # Send "bro what" status
            cstatus_payload = {
                "op": 3,
                "d": {
                    "since": 0,
                    "activities": [
                        {
                            "type": 4,
                            "state": alternate_status,
                            "name": "Custom Status",
                            "id": "custom",
                        }
                    ],
                    "status": status,
                    "afk": False,
                },
            }
            ws.send(json.dumps(cstatus_payload))
            time.sleep(1)

            # Send "discord.gg/permfruits" status
            cstatus_payload["d"]["activities"][0]["state"] = custom_status
            ws.send(json.dumps(cstatus_payload))
            time.sleep(59)

    threading.Thread(target=update_status, daemon=True).start()

def onliner(token, status):
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

def run_onliner():
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        onliner(token, status)
        time.sleep(30)

keep_alive()
run_onliner()
