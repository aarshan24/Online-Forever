from flask import Flask, request, render_template
from threading import Thread
import os
import json
import time
import threading
import websocket

app = Flask(__name__, template_folder='.')

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
    update_status()  # Set custom status when WebSocket connection opens

def update_status():
    if ws is None or not ws.sock or not ws.sock.connected:
        return  # If WebSocket connection is not open, do nothing

    # Send custom status only once
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

def onliner(token, status):
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

def run_onliner():
    while True:
        onliner(token, status)
        time.sleep(30)

def reset_status():
    global status
    status = "dnd"  # Change status to "dnd" temporarily
    print("Status changed to dnd")
    time.sleep(1)  # Wait for 1 second
    status = "online"  # Change status back to "online"
    print("Status changed to online")
    update_status()  # Reset custom status when status is reset

@app.route("/")
def keep_alive():
    return "Service is running"

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")
        if user == "godaarshan" and password == "godbot":
            return render_template("admin_panel.html")
        else:
            return render_template("login.html", message="Invalid credentials")
    return render_template("login.html", message="")

@app.route("/execute-command", methods=["POST"])
def execute_command():
    command = request.form.get("command")
    if command.startswith("cstatus"):
        _, new_custom_status = command.split(" ", 1)
        global custom_status
        custom_status = new_custom_status.strip()
        update_status()
    elif command == "dnd":
        global status
        status = "dnd"
        update_status()
    elif command == "online":
        global status
        status = "online"
        update_status()
    return "Command executed successfully"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

if __name__ == "__main__":
    keep_alive()
    threading.Thread(target=run_onliner, daemon=True).start()
