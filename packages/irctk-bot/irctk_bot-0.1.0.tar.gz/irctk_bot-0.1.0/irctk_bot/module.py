from collections import defaultdict
from typing import Any, Dict, List, Optional

from irctk_bot.command import Command


class Module:
    def __init__(self):
        self.commands = []
        self.irc_commands: Dict[str, List[Any]] = defaultdict(list)

    def command(self, name: Optional[str] = None, show_help: bool = True):
        """
        Register a command with the module.

        >>> @module.command()
        >>> def ping(context: Context):
        >>>    context.reply('pong')
        """

        def register(func):
            self.commands.append(
                Command(name or func.__name__, func, show_help=show_help)
            )
            return func

        return register

    def irc_command(self, command: str):
        """
        Register a hook for any IRC message.

        >>> @module.irc_command('PRIVMSG')
        >>> def echo(client: irctk.Client, message: irctk.Message):
        >>>    client.send_privmsg(message.prefix.nick, message.get(2))
        """

        def register(func):
            self.irc_commands[command].append(func)
            return func

        return register
