from charlesbot.base_plugin import BasePlugin
from charlesbot.config import configuration
from charlesbot.slack.slack_message import SlackMessage
from charlesbot.util.parse import does_msg_contain_prefix
import asyncio
import aiohttp


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

        return_msg = yield from self.get_all_hn_top_stories()
        yield from self.slack.send_channel_message(message.channel, str(return_msg))

    @asyncio.coroutine
    def get_all_hn_top_stories(self):
        hn_top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = yield from aiohttp.get(hn_top_stories_url)
        if not response.status == 200:
            text = yield from response.text()
            self.log.error("URL: %s" % url)
            self.log.error("Response status code was %s" % str(response.status))
            self.log.error(response.headers)
            self.log.error(text)
            response.close()
            return []
        return (yield from response.json())
