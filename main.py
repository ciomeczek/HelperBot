import os
from bot import client
from bot.actions import on_msg


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    await on_msg(message)


client.run(os.getenv('BOT_TOKEN'))
