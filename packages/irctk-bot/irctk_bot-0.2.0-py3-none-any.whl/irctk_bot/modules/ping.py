from irctk_bot.context import Context
from irctk_bot.module import Module

module = Module()


@module.command()
def ping(context: Context) -> None:
    context.reply('pong')
