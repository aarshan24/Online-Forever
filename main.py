import os
import sys
import json
import time
import threading
import websocket
import requests
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
    pass

def on_error(ws, error):
    print("Error:", error)

def on_close(*args):
    print("WebSocket connection closed")

def on_open(ws):
    print("WebSocket connection opened")
    threading.Thread(target=update_status, daemon=True).start()

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

    print("Sending auth payload:", auth_payload)
    ws.send(json.dumps(auth_payload))

def update_status():
    global status

    while True:
        print("Sending alternate status:", alternate_status)
        send_status(alternate_status)
        time.sleep(1)

        print("Sending custom status:", custom_status)
        send_status(custom_status)
        time.sleep(59)

def send_status(new_status):
    global status
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

    cstatus_payload = {
        "op": 3,
        "d": {
            "since": 0,
            "activities": [
                {
                    "type": 4,
                    "state": new_status,
                    "name": "Custom Status",
                    "id": "custom",
                }
            ],
            "status": status,
            "afk": False,
        },
    }

    print("Sending custom status payload:", cstatus_payload)
    ws.send(json.dumps(cstatus_payload))
    ws.close()

def run_onliner():
    keep_alive()
    while True:
        update_status()

run_onliner()
