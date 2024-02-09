import os
import sys
import json
import time
import requests
import threading
import websocket
from keep_alive import keep_alive
import discord
import asyncio

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

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

async def check_bot_dm():
    await client.wait_until_ready()
    bot_dm_channel = await client.fetch_user(1205105563743158312)
    last_message = await bot_dm_channel.history(limit=1).flatten()

    if len(last_message) > 0:
        last_message_content = last_message[0].content
        if "Bloxtime Army" in last_message_content:
            if "You either went offline or you removed your status, so you lost the Bloxtime Army Role." in last_message_content:
                # Change status to "bro what"
                await client.change_presence(activity=discord.Game(name="bro what"))

                # Wait for 2 seconds
                await asyncio.sleep(2)

                # Change status back to "discord.gg/permfruits"
                await client.change_presence(activity=discord.Game(name="discord.gg/permfruits"))

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    await check_bot_dm()

def on_message(ws, message):
    print("Received:", message)

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

def onliner(token, status):
    ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

def run_onliner():
    client.loop.create_task(check_bot_dm())
    client.run(token)

keep_alive()
run_onliner()
