import os
import sys
import json
import requests
import websocket
from keep_alive import keep_alive

status = "online"  # online/dnd/idle
custom_status = "discord.gg/permfruits"  # Custom status

token = os.getenv('TOKEN')
if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}

validate = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = validate.json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def set_status(status, custom_status=None):
    url = f"https://discord.com/api/v9/users/@me/settings"
    data = {
        "custom_status": {
            "text": custom_status,
            "emoji_name": None,
            "emoji_id": None
        } if custom_status else None,
        "status": status
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Status updated successfully. Status: {status}, Custom Status: {custom_status}")
    else:
        print("Failed to update status. Status code:", response.status_code)

def on_message(ws, message):
    print("Received message:", message)
    msg_data = json.loads(message)
    if msg_data.get("t") == "MESSAGE_CREATE":
        message_content = msg_data["d"]["content"]
        channel_id = msg_data["d"]["channel_id"]
        if channel_id == "1204989685852676106":  # Replace this with your actual DM channel ID
            if "welcome to" in message_content.lower():
                print("Received 'welcome to' message. Changing status to 'discord.gg/permfruits'")
                set_status(status, custom_status)
            else:
                print("No 'welcome to' message found. Changing status to 'bro what'")
                set_status(status, "bro what")

def on_error(ws, error):
    print("Error:", error)

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

def run_onliner():
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
        ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.run_forever()

keep_alive()
run_onliner()
