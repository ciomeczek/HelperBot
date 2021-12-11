from . import messages, client
from .commands import commands
import settings


async def on_msg(message):
    if message.author == client.user or not message.content.startswith(settings.PREFIX):
        return

    try:
        message_command = message.content.split(' ')[1].lower()
    except IndexError:
        await message.channel.send(messages.HELP)
        return

    for command in commands:
        if command.command == message_command:
            await command.execute(message)
            return

    await message.channel.send(messages.HELP)
