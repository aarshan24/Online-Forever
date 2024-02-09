from flask import Flask, request
from threading import Thread
import time
import requests

app = Flask('')

status = "online"  # Initial status

@app.route('/')
def main():
    global status
    # Check if the request is from the cronjobs
    if request.headers.get('User-Agent') == 'cronjob-user-agent':
        # Change status to offline
        status = "offline"
        # Sleep for 2 seconds
        time.sleep(2)
        # Change status to online
        status = "online"
    return 'I am alive'  # Return a simple response

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()
