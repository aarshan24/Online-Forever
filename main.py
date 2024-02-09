import os
import json
import time
import websocket
import requests
from keep_alive import keep_alive  # Import keep_alive module

# Global variables
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
    while True:
        try:
            change_status("placeholder")  # Set status to "placeholder"
            time.sleep(1)  # Keep status as "placeholder" for one second

            change_status(custom_status)  # Set status to custom status
            time.sleep(59)  # Keep status as custom status for 59 seconds
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    keep_alive()  # Start the Flask server
    run_main()  # Run the main function
