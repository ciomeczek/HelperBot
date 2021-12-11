from .command import Command
from .functions import *

commands = [
    Command("github", github, allowed_flags=['-p', '--project'], name='github'),
    Command("help", help, name='help'),
    Command("documentation", documentation, name='documentation'),
]
