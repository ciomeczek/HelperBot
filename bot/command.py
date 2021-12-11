from . import messages


class Command:
    def __init__(self, command, callback, allowed_flags=None, name=None):
        self.command = command
        self._callback = callback
        self.allowed_flags = allowed_flags
        self.name = name

    def _validate_flags(self, flags):
        if flags:
            return True

        if not self.allowed_flags:
            return False

        for flag in flags:
            if flag not in self.allowed_flags:
                return False
        return True

    async def execute(self, message):
        flags = message.content.split(' ')
        flags = list(filter(lambda x: (x.startswith('-')), flags))

        if self._validate_flags(message.flags):
            await self._callback(message, flags)
        else:
            await message.channel.send(messages.INVALID_FLAGS)
