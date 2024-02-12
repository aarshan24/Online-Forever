import os
import sys
import json
import time
import requests
import threading
import websocket
from utils import keep_alive


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

def on_close(ws, *args):
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
        while True:
            if get_priority() == "rollback":
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
            else:
                time.sleep(1)

    threading.Thread(target=update_status, daemon=True).start()

def onliner(token, status):
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

def lock_file_exists():
    lock_file_path = "/tmp/discord_status_lock"
    return os.path.exists(lock_file_path)

def run_script():
    if lock_file_exists():
        print("Another instance of the script is already running. Exiting.")
        return
    try:
        open("/tmp/discord_status_lock", 'a').close()  # Create lock file
        keep_alive()
        run_onliner()
    finally:
        os.remove("/tmp/discord_status_lock")  # Remove lock file

def set_priority(new_priority):
    global priority
    priority = new_priority

def get_priority():
    global priority
    return priority

if __name__ == "__main__":
    run_script()
