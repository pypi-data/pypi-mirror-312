import argparse
import asyncio
import importlib
import logging
import sys
import tomllib

import irctk
from irctk_bot.controller import Controller


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        'irctk-bot', description='irctk bot', add_help=False
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-h', '--host')
    group.add_argument('-c', '--config', type=argparse.FileType('rb'))

    parser.add_argument('-m', '--module', action='append')
    parser.add_argument('-n', '--nick', default='bot')
    return parser


def main() -> None:
    logging.basicConfig(level='INFO')
    args = create_argument_parser().parse_args()

    controller = Controller()
    if args.module:
        for module in args.module:
            controller.add_module(importlib.import_module(module))

    client = irctk.Client(nickname=args.nick)
    controller.add_client(client)
    client.delegate = controller

    if args.host:
        asyncio.run(client.connect(args.host, port=6697, use_tls=True))
        return

    config = tomllib.load(args.config)
    keys = set(config.keys())
    keys.remove('modules')
    keys.remove('host')
    keys.remove('nick')
    if keys:
        print(f'Invalid fields in config: {keys}', file=sys.stderr)
        sys.exit(1)

    if 'nick' in config:
        client.nick.nick = config['nick']

    if 'modules' in config:
        for module in config['modules']:
            controller.add_module(importlib.import_module(module))

    asyncio.run(client.connect(config['host'], port=6697, use_tls=True))
