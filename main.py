import os
import sys
import json
import time
import threading
import websocket
from flask import Flask

app = Flask(__name__)

status = "online"  # online/dnd/idle
custom_status = "discord.gg/permfruits"  # Custom status
alternate_status = "bro what"

token = os.getenv('TOKEN')
if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

def on_message(ws, message):
    print("Received:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
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
    global status

    while True:
        # Send "bro what" status
        send_status(alternate_status)
        time.sleep(1)

        # Send "discord.gg/permfruits" status
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

    ws.send(json.dumps(cstatus_payload))
    ws.close()

@app.route("/reset")
def reset_status():
    threading.Thread(target=update_status, daemon=True).start()
    return "Status reset"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
