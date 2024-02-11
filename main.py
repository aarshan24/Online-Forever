from flask import Flask
from threading import Thread
import os
import json
import time
import threading
import websocket
from tenacity import retry, stop_after_attempt, wait_fixed

app = Flask('')

status = "online"  # online/dnd/idle
custom_status = "discord.gg/permfruits"  # Custom status
token = os.getenv('TOKEN')
ws = None  # Global variable to hold WebSocket connection
is_websocket_open = False  # Flag to track WebSocket connection state

if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": token, "Content-Type": "application/json"}

def on_message(ws, message):
    pass

def on_error(ws, error):
    print("Error:", error)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def on_close(ws, *args):
    global is_websocket_open
    print("WebSocket connection closed")
    is_websocket_open = False  # Reset the flag
    onliner(token, status)

def on_open(ws):
    global is_websocket_open
    is_websocket_open = True  # Set the flag to indicate WebSocket is open
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
    global is_websocket_open
    while True:
        if is_websocket_open:
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
        else:
            print("WebSocket connection is closed. Reconnecting...")
            onliner(token, status)
            time.sleep(5)  # Wait before attempting to send status

        time.sleep(59)

def onliner(token, status):
    global ws  # Declare ws as global within this function
    global is_websocket_open  # Declare is_websocket_open as global within this function
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

def reset_status():
    global status
    status = "dnd"  # Change status to "dnd" temporarily
    print("Status changed to dnd")
    time.sleep(1)  # Wait for 1 second
    status = "online"  # Change status back to "online"
    print("Status changed to online")

@app.route("/", methods=["GET", "POST"])
def reset_or_home():
    reset_status()  # Reset status regardless of route
    print("Status reset requested")
    return "Status reset"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

if __name__ == "__main__":
    keep_alive()
    threading.Thread(target=update_status, daemon=True).start()
