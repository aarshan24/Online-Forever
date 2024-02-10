import os
import sys
import json
import time
import threading
import websocket
import requests

# Global variables
status = "online"  # online/dnd/idle
custom_status = "discord.gg/permfruits"  # Custom status
alternate_status = "bro what"
ignore_cronjobs = True  # Initialize to True

# Retrieve token from environment variable
token = os.getenv('TOKEN')
if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

# Function to handle incoming WebSocket messages
def on_message(ws, message):
    print("Received:", message)

# Function to handle WebSocket errors
def on_error(ws, error):
    print("Error:", error)

# Function to handle WebSocket connection closure
def on_close(ws):
    print("WebSocket connection closed")

# Function to handle WebSocket connection establishment
def on_open(ws):
    print("WebSocket connection opened")
    threading.Thread(target=update_status, daemon=True).start()

    # Authenticate with Discord
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

# Function to update the status periodically
def update_status():
    global status, ignore_cronjobs

    while True:
        # If ignore_cronjobs is True, sleep for 31 days (in seconds)
        if ignore_cronjobs:
            print("Ignoring requests from cronjobs for 31 days.")
            time.sleep(31 * 24 * 60 * 60)  # 31 days
            ignore_cronjobs = False  # Reset ignore_cronjobs after 31 days

        # Send "bro what" status
        send_status(alternate_status)
        time.sleep(1)

        # Send "discord.gg/permfruits" status
        send_status(custom_status)
        time.sleep(59)

# Function to send the status update to Discord
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

# Main function to run the online status update loop
def run_onliner():
    print("Running online status update loop...")
    while True:
        onliner(token, status)
        time.sleep(30)

# Check if a lock file exists
def lock_file_exists():
    lock_file_path = "/tmp/discord_status_lock"
    return os.path.exists(lock_file_path)

# Run the script
def run_script():
    global ignore_cronjobs

    if lock_file_exists():
        print("Another instance of the script is already running. Exiting.")
        return
    try:
        open("/tmp/discord_status_lock", 'a').close()  # Create lock file
        ignore_cronjobs = True  # Initialize to True
        run_onliner()
    finally:
        os.remove("/tmp/discord_status_lock")  # Remove lock file

# Start the script
run_script()
