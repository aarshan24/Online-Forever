from flask import Flask
from threading import Thread
import os
import json
import time
import threading
import websocket

app = Flask('')

status = "online"  # online/dnd/idle
custom_status = "discord.gg/permfruits"  # Custom status
token = os.getenv('TOKEN')
ws = None  # Global variable to hold WebSocket connection

if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": token, "Content-Type": "application/json"}

def on_message(ws, message):
    pass

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, *args):
    print("WebSocket connection closed")
    ws = None  # Reset WebSocket connection
    reset_status()  # Reset status when WebSocket connection closes

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

def update_status():
    while True:
        if ws is None or not ws.sock or not ws.sock.connected:
            print("WebSocket connection is closed. Reconnecting...")
            onliner(token, status)
            time.sleep(5)  # Wait before attempting to send status
            continue

        # Send custom status
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
        print("Sent custom status")
        time.sleep(59)

def onliner(token, status):
    global ws  # Declare ws as global within this function
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

def reset_status():
    global status
    status = "online"  # Reset status to online
    print("Status reset to online")

def run_onliner():
    while True:
        onliner(token, status)
        time.sleep(30)

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

if __name__ == "__main__":
    keep_alive()
    update_status_thread = threading.Thread(target=update_status)
    update_status_thread.daemon = True
    update_status_thread.start()
