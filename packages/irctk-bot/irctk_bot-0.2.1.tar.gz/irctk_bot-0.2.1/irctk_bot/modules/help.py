from inspect import Parameter, signature
from typing import Optional

import irctk
from irctk_bot.command import Command, TargetMode
from irctk_bot.context import Context
from irctk_bot.controller import Controller
from irctk_bot.module import Module

module = Module()


def command_parameters(func) -> Optional[str]:
    arguments = []

    for parameter in signature(func).parameters.values():
        if parameter.annotation in (Context, Controller, irctk.Client, irctk.Message):
            # irctk-bot injects these, not for user to input
            continue

        name = parameter.name.replace('_', ' ')

        if parameter.default == Parameter.empty:
            name = f'<{name}>'
        else:
            name = f'[{name}]'

        if parameter.kind == Parameter.VAR_POSITIONAL:
            name = f'{name}...'

        arguments.append(name)

    if arguments:
        return ' '.join(arguments)
    return None


def command_usage(command: Command) -> str:
    parameters = command_parameters(command.func)
    if parameters:
        return f'{command.name} {parameters}'
    return command.name


def show_command_in_help(context: Context):
    def evaluate(command: Command) -> bool:
        if command.target_mode == TargetMode.CHANNEL and not context.channel:
            return False

        if command.target_mode == TargetMode.NICK and context.channel:
            return False

        return command.show_help

    return evaluate


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

        parameters = command_parameters(command.func)
        if parameters:
            context.reply(f'Usage: {command.name} {parameters}')

        return

    commands = map(command_usage, filter(show_command_in_help, controller.commands))
    command = ', '.join(commands)
    context.reply(f'commands: {command}')
