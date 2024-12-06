from enum import Enum, auto
from functools import wraps
from typing import Optional


class TargetMode(Enum):
    ALL = auto()
    CHANNEL = auto()
    NICK = auto()


class Command:
    def __init__(
        self,
        name: str,
        func,
        parser,
        show_help: bool = True,
        target_mode: TargetMode = TargetMode.ALL,
    ):
        self.name = name
        self.func = func
        self.parser = parser
        self.show_help = show_help
        self.target_mode = target_mode


def requires_account(account: Optional[str] = None):
    def wrap(func):
        @wraps(func)
        def inner(context, *args, **kwargs):
            if account:
                if context.message.account != account:
                    return context.reply('unauthorized')

            elif not context.message.account:
                return context.reply('unauthorized, please login')

            return func(context, *args, **kwargs)

        return inner

    return wrap
