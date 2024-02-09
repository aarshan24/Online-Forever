from flask import Flask, request
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    global pending_status
    # Handle incoming request from cronjobs
    # Set pending_status to signal main.py to change status
    pending_status = "change"
    return 'I am alive'  # Return a simple response

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    global pending_status
    pending_status = ""  # Initialize pending_status
    server = Thread(target=run)
    server.start()

pending_status = ""  # Initialize pending_status
