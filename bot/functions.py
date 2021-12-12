from . import messages
from .command import Command
from . import client


async def github(command: Command):
    if command.has_short_or_long('-p', '--project'):
        await command.message.channel.send(messages.GH_ORGANIZATION)
    else:
        await command.message.channel.send(messages.GITHUB)


async def help(command: Command):
    await command.message.channel.send(messages.MAN)


async def documentation(command: Command):
    await command.message.channel.send(messages.DOCUMENTATION)


async def guild_id(command: Command):
    await command.message.channel.send(f'The guild ID is: {command.message.guild.id}')


async def channel_id(command: Command):
    await command.message.channel.send(f'The channel ID is: {command.message.channel.id}')


async def anonymous_message(command: Command):
    channel = command.channel

    channel = client.get_channel(channel)

    if channel is None:
        await command.message.channel.send(f'Im not in this guild.')
        return

    if command.user is not None:
        user = client.get_user(command.user)

        if user is None:
            await command.message.channel.send(f'There is no user with this ID.')
            return

        await channel.send(f'<@{user.id}> {command.content}')
        return

    await channel.send(command.content)
