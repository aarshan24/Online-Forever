import os
import json
import time
import websocket
import requests
from keep_alive import pending_status


status = "online"  # Default status
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

def change_status(new_status):
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.create_connection(ws_url)
    auth_payload = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows",
            },
            "presence": {"status": new_status, "afk": False},
        }
    }
    ws.send(json.dumps(auth_payload))
    ws.close()

def run_main():
    global pending_status
    while True:
        print("Pending status:", pending_status)  # Add this line
        if pending_status:
            change_status("bro what")
            time.sleep(1)  # Change status to "bro what" for a second
            change_status(custom_status)  # Change status to custom status
            pending_status = ""  # Reset pending status
        else:
            change_status(custom_status)  # Set status to default
            time.sleep(10)  # Wait for 10 seconds before checking again

run_main()
