from flask import Flask
from threading import Thread
import os
import json
import time
import websocket
import logging
from tenacity import retry, stop_after_delay, wait_fixed

app = Flask('')

status = "online"  # online/dnd/idle
custom_status = "discord.gg/permfruits"  # Custom status
token = os.getenv('TOKEN')
ws = None  # Global variable to hold WebSocket connection

if not token:
    logging.error("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": token, "Content-Type": "application/json"}

@retry(stop=stop_after_delay(5), wait=wait_fixed(2))
def on_message(ws, message):
    pass

@retry(stop=stop_after_delay(5), wait=wait_fixed(2))
def on_error(ws, error):
    logging.error("WebSocket error: %s", error)

@retry(stop=stop_after_delay(5), wait=wait_fixed(2))
def on_close(ws, *args):
    logging.warning("WebSocket connection closed")
    ws = None  # Reset WebSocket connection
    time.sleep(5)  # Wait before attempting to reconnect
    onliner(token, status)  # Reconnect WebSocket

@retry(stop=stop_after_delay(5), wait=wait_fixed(2))
def on_open(ws):
    # Declare ws as global within this function
    logging.info("WebSocket connection opened")

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
    global ws  # Declare ws as global within this function
    while True:
        try:
            if ws is None or not ws.sock or not ws.sock.connected:
                logging.warning("WebSocket connection is closed. Reconnecting...")
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
            logging.info("Sent custom status")
        except Exception as e:
            logging.error("Error updating status: %s", e)
            time.sleep(5)  # Wait before retrying

def onliner(token, status):
    global ws  # Declare ws as global within this function
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

def run_onliner():
    Thread(target=update_status, daemon=True).start()

def reset_loop():
    global status
    status = "dnd"  # Change status to "dnd" temporarily
    logging.info("Status changed to dnd")
    time.sleep(1)  # Wait for 1 second
    status = "online"  # Change status back to "online"
    logging.info("Status changed to online")

@app.route("/reset")
def reset_status():
    Thread(target=reset_loop, daemon=True).start()
    logging.info("Reset flag set to True")
    return "Status reset"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    keep_alive()
    run_onliner()
