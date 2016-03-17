from charlesbot.base_plugin import BasePlugin
from charlesbot.config import configuration
from charlesbot.slack.slack_message import SlackMessage
from charlesbot.util.parse import does_msg_contain_prefix
import asyncio


class HelloWorld(BasePlugin):

    def __init__(self):
        super().__init__("HelloWorld")
        self.load_config()

    def load_config(self):  # pragma: no cover
        config_dict = configuration.get()
        self.token = config_dict['helloworld']['config_key']

    def get_help_message(self):
        help_msg = []
        help_msg.append("!command - Does a really neat thing!")
        return "\n".join(help_msg)

    @asyncio.coroutine
    def process_message(self, message):
        self.log.info("Processing message %s" % message)

        if not type(message) is SlackMessage:
            return

        if not does_msg_contain_prefix("!hn", message.text):
            return

        return_msg = "Hi there!"
        yield from self.slack.send_channel_message(message.channel, return_msg)
