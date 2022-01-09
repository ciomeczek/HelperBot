import os
import io
import discord
import aiohttp
from bot import client
from bot.actions import on_msg


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    await on_msg(message)


@client.event
async def on_message_delete(message):
    if message.author.bot:
        return

    files = []
    async with aiohttp.ClientSession() as session:
        for attachment in message.attachments:
            async with session.get(attachment.url) as resp:
                data = io.BytesIO(await resp.read())
                files.append(discord.File(data, filename=attachment.url.split('/')[-1]))

    await message.channel.send(f'<@{message.author.id}> deleted message: "{message.content}" at '
                               f'{message.created_at.strftime("%m/%d/%Y, %H:%M:%S")}', files=files)


client.run(os.getenv('BOT_TOKEN'))
