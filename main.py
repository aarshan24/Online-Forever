import os
import asyncio
import discord

status = "online"  # online/dnd/idle
custom_status = "discord.gg/permfruits"  # Custom status

token = os.getenv('TOKEN')
channel_id = 1205105563743158312  # Channel ID of the bot's DM

if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

async def check_bot_dm():
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        channel = client.get_channel(channel_id)
        if not channel:
            print("Channel not found.")
            return
        try:
            last_message = await channel.history(limit=1).flatten()
            message = last_message[0]
            if message.author == client.user:  # Ignore messages sent by self
                return
            # Check if the last message in the DM is the one we're interested in
            if "Bloxtime Army" in message.content:
                if "You either went offline or you removed your status" in message.content:
                    print("Offline message received. Changing status to 'bro what'")
                    await client.change_presence(activity=discord.Game("bro what"))
                elif "Welcome to the Bloxtime Army. You have been given the role." in message.content:
                    print("Role granted. Changing status to 'discord.gg/permfruits'")
                    await client.change_presence(activity=discord.Game(custom_status))
        except Exception as e:
            print(f"Error: {e}")

    await client.start(token)

async def onliner():
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        await check_bot_dm()  # Check DMs for bot messages
        await asyncio.sleep(30)  # Wait for 30 seconds
        await client.close()  # Close the connection

    await client.start(token)

# Run the bot
asyncio.run(onliner())
