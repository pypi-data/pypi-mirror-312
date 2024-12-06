from typing import Optional

from irctk.client import Client
from irctk.command import Command
from irctk.message import Message, MessageTag


class Context:
    def __init__(
        self, sender: str, channel: Optional[str], message: Message, client: Client
    ):
        self.sender = sender
        self.channel = channel
        self.message = message
        self.client: Client = client

    def reply(self, text: str) -> None:
        if self.channel:
            target = self.channel
            text = f'{self.sender}: {text}'
        else:
            target = self.sender

        for line in text.splitlines():
            message = Message(command=Command.NOTICE.value, parameters=[target, line])
            msgid = self.message.find_tag('msgid')
            if msgid:
                message.tags.append(MessageTag(True, 'draft', 'reply', msgid))

            self.client.send(message)
