from typing import Optional

from irctk_bot.context import Context
from irctk_bot.controller import Controller
from irctk_bot.module import Module

module = Module()


@module.command()
def help(
    context: Context, controller: Controller, command_name: Optional[str] = None
) -> None:
    if command_name:
        command = controller.find_command(command_name)
        if not command:
            context.reply(f'no such command: {command_name}')
            return

        if not command.func.__doc__:
            context.reply(f'no help available for the {command.name} command')
            return

        context.reply(command.func.__doc__.strip())
        return

    commands = ', '.join([c.name for c in controller.commands if c.show_help])
    context.reply(f'commands: {commands}')
