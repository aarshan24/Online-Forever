import os
import json
import time
import threading
import websocket
import requests
from flask import Flask

app = Flask(__name__)

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

ws = None  # Global WebSocket connection
reset_request_received = False  # Flag to indicate a reset request

def on_message(ws, message):
    pass

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, *args):
    print("WebSocket connection closed")
    if reset_request_received:
        # If a reset request was received, re-run the script
        run_script()

def on_open(ws):
    print("WebSocket connection opened")
    # Start the status update loop in a separate thread
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
    global status, reset_request_received
    while True:
        # Check if a reset request was received
        if reset_request_received:
            reset_request_received = False
            break
        
        # Send "bro what" status for 1 second
        send_status(alternate_status)
        time.sleep(1)

        # Send "discord.gg/permfruits" status for 59 seconds
        send_status(custom_status)
        time.sleep(59)

def send_status(new_status):
    global status, ws
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

def run_script():
    global ws
    if ws and ws.sock and ws.sock.connected:
        ws.close()
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

@app.route("/reset")
def reset_status():
    global reset_request_received
    reset_request_received = True
    return "Status reset"

def keep_alive():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()
    run_script()
