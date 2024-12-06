import asyncio
import logging
from typing import Any, Generator, Optional

import irctk
from irctk.client import Client
from irctk_bot.command import TargetMode
from irctk_bot.context import Context

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, nick: str, host: str, channels):
        self.clients = []
        self.modules = []

        self.nick = nick
        self.host = host
        self.channels = channels
        self.loop = asyncio.new_event_loop()

    def connect(self) -> None:
        client = Client(self.nick)
        client.delegate = self
        self.clients.append(client)
        self.loop.create_task(client.connect(self.host, port=6697, use_tls=True))

    def add_module(self, module) -> None:
        self.modules.append(module)

    def find_module(self, name: str):
        for module in self.modules:
            if module.__name__ == name:
                return module

        return None

    @property
    def commands(self) -> Generator[Any, None, None]:
        for module in self.modules:
            for command in module.module.commands:
                yield command

    def irc_command_handlers(self, command: str):
        for module in self.modules:
            if command not in module.module.irc_commands:
                continue
            for handler in module.module.irc_commands[command]:
                yield handler

    def find_command(self, name: str) -> Optional[Any]:
        for command in self.commands:
            if command.name == name:
                return command

        return None

    def run_command_handlers(
        self, client: irctk.Client, message: irctk.Message
    ) -> None:
        for handler in self.irc_command_handlers(message.command):
            try:
                handler(client=client, message=message)
            except Exception as e:
                logger.error('Cannot invoke %s', handler, e)

    # ClientDelegate

    def irc_disconnected(self, client, error):
        logger.error('Disconnected %s', error)
        self.clients.remove(client)

        async def reconnect():
            await asyncio.sleep(5)
            self.connect()

        self.loop.create_task(reconnect())

    def irc_registered(self, client):
        client.send('MODE', client.nick, '+B')
        for channel in self.channels:
            client.send_join(channel)

    def irc_message(self, client: irctk.Client, message: irctk.Message) -> None:
        self.run_command_handlers(client, message)

        if message.command != 'PRIVMSG':
            return

        if not message.prefix:
            return

        sender = client.nick_class.parse(message.prefix).nick
        target = message.get(0)
        text = message.get(1)
        if not target or not text:
            return

        if client.irc_equal(target, client.nick.nick):
            context = Context(sender, None, message, client)
        else:
            context = Context(sender, target, message, client)

        if context.channel and not text.startswith(f'{client.nick.nick}: '):
            return

        if text.startswith(f'{client.nick.nick}: '):
            text = text[len(client.nick.nick) + 2 :]

        command_name, _, args = text.partition(' ')
        command = self.find_command(command_name)
        if not command:
            context.reply(f'command {command_name} not found')
            return

        if command.target_mode == TargetMode.CHANNEL:
            if not context.channel:
                return context.reply(f'{command_name} can only be used in a channel')
        elif command.target_mode == TargetMode.NICK:
            if context.channel:
                return context.reply(f'{command_name} can only be used in DM')
        elif command.target_mode != TargetMode.ALL:
            logger.error('Unexpected target mode %s', command.target_mode)
            context.reply('internal error')
            return

        try:
            args, kwargs = command.parser.parse(
                args,
                dependencies={
                    Context: context,
                    irctk.Message: message,
                    Client: client,
                    Controller: self,
                },
            )
        except ValueError as e:
            if len(e.args) == 2:
                context.reply(f'{e.args[0]}: {e.args[1]}')
            else:
                context.reply(str(e))
            return
        except TypeError as e:
            logger.error('Cannot invoke %s', command.func, e)
            context.reply('internal error')
            return

        logger.info('Running %s (%s %s)', command.func, args, kwargs)
        try:
            command.func(*args, **kwargs)
        except Exception as e:
            logger.error('Cannot invoke %s', command.func, e)
            context.reply('internal error')
