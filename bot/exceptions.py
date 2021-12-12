class InvalidFlagError(Exception):
    pass


class NoFlagError(InvalidFlagError):
    pass


class NoFlagArgument(InvalidFlagError):
    pass


class InvalidFlagArgumentType(InvalidFlagError):
    pass


class MissingFlags(InvalidFlagError):
    pass
