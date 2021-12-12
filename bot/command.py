from . import messages
from .exceptions import *


class Flag:
    def __init__(self, short: str, long: str, has_argument=False, required=False, argument_type=str):
        self.short = short
        self.long = long
        self.has_argument = has_argument
        self.required = required
        self.argument_type = argument_type
        self.argument = None


class Command:
    def __init__(self, command: str, callback: callable, allowed_flags=None, name=None, message=None):
        self.command = command
        self._callback = callback
        self.allowed_flags = allowed_flags if allowed_flags else []
        self.name = name
        self._flags = None
        self.message = message

    def _validate_flags(self, flags: list[str]) -> bool:
        required_flags = list(filter(lambda x: x.required, self.allowed_flags))
        for required_flag in required_flags:
            if not any(required_flag.short == x or required_flag.long == x for x in flags):
                raise MissingFlags(f'Flag {required_flag.short}/{required_flag.long} is required')

        for flag in flags:
            if not any(x.short == flag or x.long == flag for x in self.allowed_flags):
                raise InvalidFlagError(f'Flag {flag} is not allowed')

    def _strings_to_flags(self, strings: list[str], message) -> list[Flag]:
        flags = []
        for string in strings:
            flag = list(filter(lambda x: (x.short == string or x.long == string), self.allowed_flags))[0]

            if flag.has_argument:
                try:
                    if flag.short + ' ' in message.content:
                        argument = message.content.split(flag.short)[1].split('-')[0]
                        try:
                            flag.argument = flag.argument_type(argument)
                        except ValueError:
                            raise InvalidFlagArgumentType(f'Invalid argument type')
                    else:
                        argument = message.content.split(flag.long)[1].split('-')[0]
                        try:
                            flag.argument = flag.argument_type(argument)
                        except ValueError:
                            raise InvalidFlagArgumentType(f'Invalid argument type')
                except IndexError:
                    raise InvalidFlagError(f'Flag {flag.short} or {flag.long} requires an argument')

            flags.append(flag)
        return flags

    def has_flag(self, flag: str) -> bool:
        return any(x.short == flag or x.long == flag for x in self._flags)

    def has_short_or_long(self, short: str, long: str) -> bool:
        return any(x.short == short or x.long == long for x in self._flags or [])

    def get_flag_argument(self, flag: str) -> str:
        for x in self._flags:
            if x.short == flag or x.long == flag:
                if x.argument is None:
                    raise NoFlagArgument(f'Flag {flag} has no argument')

                return x.argument

        raise NoFlagError(f'Flag {flag} not found')

    async def execute(self, message):
        flags = message.content.split(' ')
        flags = list(filter(lambda x: (x.startswith('-')), flags))

        try:
            self._validate_flags(flags)
            self.message = message

            for flag in self.allowed_flags:
                setattr(self, flag.short.replace('-', ''), None)
                setattr(self, flag.long.replace('-', ''), None)

            flags = self._strings_to_flags(flags, message)
            self._flags = flags

            for flag in flags:
                setattr(self, flag.short.replace('-', ''), flag.argument)
                setattr(self, flag.long.replace('-', ''), flag.argument)

            await self._callback(self)
        except MissingFlags:
            await message.channel.send(messages.MISSING_FLAGS)
        except InvalidFlagError:
            await message.channel.send(messages.INVALID_FLAGS)
