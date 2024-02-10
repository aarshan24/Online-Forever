import os
import sys
import json
import time
import threading
import websocket
import requests

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

ws = None

def on_message(ws, message):
    print("Received:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, *args):
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

    ws.send(json.dumps(auth_payload))

def update_status():
    global status, ws
    while True:
        # Send "bro what" status
        send_status(alternate_status)
        time.sleep(1)

        # Send "discord.gg/permfruits" status
        send_status(custom_status)
        time.sleep(59)

def send_status(new_status):
    global status, ws
    if ws is None or not ws.sock or not ws.sock.connected:
        ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
        ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.run_forever()

    if ws.sock and ws.sock.connected:
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

        ws.send(json.dumps(cstatus_payload))
    else:
        print("WebSocket connection is closed. Unable to send status update.")

if __name__ == "__main__":
    update_status()
