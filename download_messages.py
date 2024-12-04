import discord
import asyncio
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Get Discord token and channel ID from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    
    if not channel:
        print(f"Couldn't find channel with ID {CHANNEL_ID}")
        await client.close()
        return

    print(f"Downloading messages from channel: {channel.name}")

    # Calculate the date one month ago
    one_month_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=90)

    messages = []
    async for message in channel.history(limit=None, after=one_month_ago):
        messages.append(f"{message.created_at} - {message.author.name}: {message.content}")

    with open('discord_messages_last_month.txt', 'w', encoding='utf-8') as f:
        for message in reversed(messages):
            f.write(f"{message}\n")

    print(f"Downloaded {len(messages)} messages from the last month to discord_messages_last_month.txt")
    await client.close()

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)

