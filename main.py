import os
import sys
import json
import time
import requests
import threading
import discord
import asyncio

from keep_alive import keep_alive

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

async def check_bot_dm():
    # Channel ID of the DM channel with the bot
    channel_id = '1205105563743158312'

    # Create a Discord client
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.channel.id == int(channel_id):
            if message.content.startswith('Bloxtime Army'):
                if "You either went offline or you removed your status" in message.content:
                    # Change status to 'bro what'
                    print("Changing status to 'bro what'")
                    await client.change_presence(activity=discord.Game(name="bro what"))

                    # Wait for 2 seconds
                    await asyncio.sleep(2)

                    # Change status back to 'discord.gg/permfruits'
                    print("Changing status back to 'discord.gg/permfruits'")
                    await client.change_presence(activity=discord.Game(name="discord.gg/permfruits"))

                elif "Welcome to the Bloxtime Army" in message.content:
                    # Do nothing if the expected message is received
                    pass

    await client.start(token)

async def onliner():
    await check_bot_dm()
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        print("Connecting...")
        await asyncio.sleep(30)

# Start the Flask server to keep the web server alive
keep_alive()

# Get the event loop and run the onliner coroutine until it completes
loop = asyncio.get_event_loop()
loop.run_until_complete(onliner())
