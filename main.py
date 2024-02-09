import os
import asyncio
import discord

token = os.getenv('TOKEN')

if not token:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

async def main():
    intents = discord.Intents.default()
    intents.messages = True  # Enable message-related intents

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

        dm_channel_id = 1204989685852676106  # Correct DM channel ID
        dm_channel = client.get_channel(dm_channel_id)
        if not dm_channel:
            print("DM channel not found.")
            return

        async for message in dm_channel.history(limit=1):
            if "welcome to" in message.content.lower():
                print("Received 'welcome to' message. Changing status to 'discord.gg/permfruits'")
                await client.change_presence(activity=discord.Game("discord.gg/permfruits"))
            else:
                print("No 'welcome to' message found. Changing status to 'bro what'")
                await client.change_presence(activity=discord.Game("bro what"))

        await asyncio.sleep(5)  # Wait for 5 seconds before closing the connection
        await client.close()

    await client.start(token)

# Run the bot
asyncio.run(main())
