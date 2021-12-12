from . import messages


class InvalidFlagError(Exception):
    pass


class NoFlagError(Exception):
    pass


class NoFlagArgument(Exception):
    pass


class Flag:
    def __init__(self, short: str, long: str, has_argument=False, argument=None, required=False, argument_type=str):
        self.short = short
        self.long = long
        self.has_argument = has_argument
        self.argument = argument
        self.required = required
        self.argument_type = argument_type


class Command:
    def __init__(self, command: str, callback: callable, allowed_flags=[], name=None, flags=None, message=None):
        self.command = command
        self._callback = callback
        self.allowed_flags = allowed_flags
        self.name = name
        self.flags = flags
        self.message = message

    def _validate_flags(self, flags: list[str]) -> bool:
        if not flags:
            return True

        if not self.allowed_flags:
            return False

        for flag in flags:
            if not any(x.short == flag or x.long == flag for x in self.allowed_flags):
                return False

        for flag in list(filter(lambda x: x.required, self.allowed_flags)):
            if not any(flag.short == x or flag.long == x for x in flags):
                return False

        return True

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
                            raise InvalidFlagError(f'Invalid argument type')
                    else:
                        argument = message.content.split(flag.long)[1].split('-')[0]
                        try:
                            flag.argument = flag.argument_type(argument)
                        except ValueError:
                            raise InvalidFlagError(f'Invalid argument type')
                except IndexError:
                    raise InvalidFlagError(f'Flag {flag.short} or {flag.long} requires an argument')

            flags.append(flag)
        return flags

    def has_flag(self, flag: str) -> bool:
        return any(x.short == flag or x.long == flag for x in self.flags)

    def has_short_or_long(self, short: str, long: str) -> bool:
        return any(x.short == short or x.long == long for x in self.flags)

    def get_flag_argument(self, flag: str) -> str:
        for x in self.flags:
            if x.short == flag or x.long == flag:
                if x.argument is None:
                    raise NoFlagArgument(f'Flag {flag} has no argument')

                return x.argument

        raise NoFlagError(f'Flag {flag} not found')

    async def execute(self, message):
        flags = message.content.split(' ')
        flags = list(filter(lambda x: (x.startswith('-')), flags))

        if self._validate_flags(flags):
            self.message = message

            try:
                flags = self._strings_to_flags(flags, message)

                for flag in self.allowed_flags:
                    setattr(self, flag.short.replace('-', ''), None)
                    setattr(self, flag.long.replace('-', ''), None)

                for flag in flags:
                    setattr(self, flag.short.replace('-', ''), flag.argument)
                    setattr(self, flag.long.replace('-', ''), flag.argument)
            except InvalidFlagError:
                await message.channel.send(messages.INVALID_FLAGS)
                return

            await self._callback(self)
        else:
            await message.channel.send(messages.INVALID_FLAGS)
