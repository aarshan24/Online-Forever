from flask import Flask, request
from threading import Thread

app = Flask('')

@app.route('/', methods=['POST'])
def main():
    global pending_status
    print("Request detected")
    pending_status = "discord.gg/permfruits"  # Set pending_status to discord.gg/permfruits
    return 'OK'

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()
