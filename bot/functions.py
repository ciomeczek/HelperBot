from . import messages


async def github(message, flags):
    if '-p' in flags or '--project' in flags:
        await message.channel.send(messages.GH_ORGANIZATION)
    else:
        await message.channel.send(messages.GITHUB)


async def help(message, flags):
    await message.channel.send(messages.MAN)


async def documentation(message, flags):
    await message.channel.send(messages.DOCUMENTATION)
