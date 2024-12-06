from collections import defaultdict
from typing import Any, Dict, List, Optional

from irctk_bot.argument_parser import ArgumentParser
from irctk_bot.command import Command, TargetMode


class Module:
    def __init__(self):
        self.commands = []
        self.irc_commands: Dict[str, List[Any]] = defaultdict(list)

    def command(
        self,
        name: Optional[str] = None,
        show_help: bool = True,
        target_mode: TargetMode = TargetMode.ALL,
    ):
        """
        Register a command with the module.

        :param name: The name of the command, this will default to the function name if unset.
        :param show_help: Whether to show the command in help list output.
        :param target_mode: The targets that the command can be used within.

        >>> @module.command()
        >>> def ping(context: Context):
        >>>    context.reply('pong')
        """

        def register(func):
            parser = ArgumentParser(func)
            parser.validate()

            self.commands.append(
                Command(
                    name or func.__name__,
                    func,
                    parser,
                    show_help=show_help,
                    target_mode=target_mode,
                )
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
