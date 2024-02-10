import os
import sys
import json
import time
import requests
import threading
import websocket
from flask import Flask
from threading import Thread

app = Flask('')

status = "online"  # online/dnd/idle
custom_status = "discord.gg/permfruits"  # Custom status

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

reset_flag = False

def on_message(ws, message):
    pass

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws):
    print("WebSocket connection closed")

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
        global reset_flag
        while True:
            try:
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
                if reset_flag:
                    cstatus_payload["d"]["activities"][0]["state"] = "dnd"
                    ws.send(json.dumps(cstatus_payload))
                    print("Status changed to dnd")
                    time.sleep(1)  # Wait for 1 second
                    cstatus_payload["d"]["activities"][0]["state"] = custom_status
                    ws.send(json.dumps(cstatus_payload))
                    print("Status changed to online")
                    reset_flag = False
                else:
                    ws.send(json.dumps(cstatus_payload))
                    print("Sent custom status")
                time.sleep(59)
            except Exception as e:
                print("Error sending custom status:", e)
                time.sleep(10)  # Retry after 10 seconds

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

def lock_file_exists():
    lock_file_path = "/tmp/discord_status_lock"
    return os.path.exists(lock_file_path)

def run_script():
    if lock_file_exists():
        print("Another instance of the script is already running. Exiting.")
        return
    try:
        open("/tmp/discord_status_lock", 'a').close()  # Create lock file
        run_onliner()
    finally:
        os.remove("/tmp/discord_status_lock")  # Remove lock file

@app.route("/reset")
def reset_status():
    global reset_flag
    reset_flag = True
    return "Status reset"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

if __name__ == "__main__":
    keep_alive()
    run_script()
