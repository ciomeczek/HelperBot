from .command import Command, Flag
from .functions import *

commands = [
    Command("github", github, allowed_flags=[Flag('-p', '--project')], name='github'),
    Command("help", help, name='help'),
    Command("documentation", documentation, name='documentation'),
    Command("guildid", guild_id, name='guild_id'),
    Command("channelid", channel_id, name='channel_id'),
    Command("userid", user_id, allowed_flags=[
        Flag('-u', '--user', has_argument=True, argument_type=str, required=True)
    ], name='channel_id'),
    Command("anonymous", anonymous_message, allowed_flags=[
        Flag('-c', '--channel', has_argument=True, required=True, argument_type=int),
        Flag('-u', '--user', has_argument=True, argument_type=int),
        Flag('-C', '--content', has_argument=True, required=True, argument_type=str)],
            name='anonymous'),
]
