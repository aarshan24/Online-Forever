import os
import sys
import json
import requests
import threading
import websocket
from flask import Flask
import time

app = Flask('')

status = "online"  # online/dnd/idle
custom_status = "discord.gg/permfruits"  # Custom status
alternate_status = "bro what"
ws = None  # Initialize WebSocket connection object as global variable

token = os.getenv('TOKEN')
if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": token, "Content-Type": "application/json"}

def on_message(ws, message):
    print("Received:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, *args):
    print("WebSocket connection closed")

def on_open(ws):
    print("WebSocket connection opened")

def update_status():
    global ws
    while True:
        # Send "discord.gg/permfruits" status
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
        if ws:  # Check if WebSocket connection is valid
            ws.send(json.dumps(cstatus_payload))
        time.sleep(59)

def reset_status():
    global ws, status
    status = "dnd"  # Change status to "dnd" temporarily
    print("Status changed to dnd")
    time.sleep(1)  # Wait for 1 second
    status = "online"  # Change status back to "online"
    print("Status changed to online")

    # Send "discord.gg/permfruits" status
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
    if ws:  # Check if WebSocket connection is valid
        ws.send(json.dumps(cstatus_payload))

def onliner(token, status):
    global ws
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    update_thread = threading.Thread(target=update_status, daemon=True)
    update_thread.start()
    ws.run_forever()

def run_onliner():
    onliner(token, status)

@app.route("/reset")
def reset():
    threading.Thread(target=reset_status).start()
    return "Status reset"

if __name__ == "__main__":
    run_onliner()
    app.run(host="0.0.0.0", port=8080)
