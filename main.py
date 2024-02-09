import os
import asyncio
import discord

status = "online"  # online/dnd/idle
custom_status = "discord.gg/permfruits"  # Custom status

token = os.getenv('TOKEN')

if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

async def check_dm():
    intents = discord.Intents.default()
    intents.messages = True  # Enable message-related intents

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        dm_channel = client.get_channel(1204989685852676106)  # Correct DM channel ID
        if not dm_channel:
            print("DM channel not found.")
            await client.close()
            return

        async for message in dm_channel.history(limit=1):
            if "welcome to" in message.content.lower():
                print("Received 'welcome to' message. Changing status to 'discord.gg/permfruits'")
                await client.change_presence(activity=discord.Game(custom_status))
            else:
                print("No 'welcome to' message found. Changing status to 'bro what'")
                await client.change_presence(activity=discord.Game("bro what"))

        await asyncio.sleep(5)  # Wait for 5 seconds
        await client.close()  # Close the connection

    await check_dm()  # Run the check_dm coroutine directly

# Run the bot
asyncio.run(check_dm())
