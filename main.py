import os
import asyncio
import discord
from discord.gateway import DiscordWebSocket

token = os.getenv('TOKEN')

if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

async def check_dm(websocket):
    dm_channel_id = 1204989685852676106  # Correct DM channel ID

    # Listen for messages in the DM channel
    async for message in websocket.dms(dm_channel_id):
        if "welcome to" in message.content.lower():
            print("Received 'welcome to' message. Changing status to 'discord.gg/permfruits'")
            await client.change_presence(activity=discord.Game("discord.gg/permfruits"))
        else:
            print("No 'welcome to' message found. Changing status to 'bro what'")
            await client.change_presence(activity=discord.Game("bro what"))

    await asyncio.sleep(5)  # Wait for 5 seconds before closing the connection

async def main():
    client = discord.Client(intents=None)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

        websocket = DiscordWebSocket.from_client(client)
        await websocket.open()

        await check_dm(websocket)

        await websocket.close()

    await client.start(token)

# Run the bot
asyncio.run(main())
