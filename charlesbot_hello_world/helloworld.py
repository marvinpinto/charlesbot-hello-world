from charlesbot.base_plugin import BasePlugin
from charlesbot.config import configuration
from charlesbot.slack.slack_message import SlackMessage
from charlesbot.slack.slack_attachment import SlackAttachment
from charlesbot.util.parse import does_msg_contain_prefix
import asyncio
import aiohttp
from aiocron import crontab


class HelloWorld(BasePlugin):

    def __init__(self):
        super().__init__("HelloWorld")
        self.load_config()
        self.schedule_timer_message()

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

        raw_story_ids = yield from self.get_all_hn_top_stories()
        return_attachment = yield from self.print_top_n_hn_stories(5, raw_story_ids)
        yield from self.slack.api_call(
            'chat.postMessage',
            channel=message.channel,
            attachments=return_attachment,
            as_user=False,
            username="Hacker News",
            icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2016-03-18/27749445461_48.png"
        )

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

    @asyncio.coroutine
    def print_top_n_hn_stories(self, number_of_stories, raw_story_ids):
        return_string = []
        for story in raw_story_ids[:number_of_stories]:
            url = "https://hacker-news.firebaseio.com/v0/item/%s.json" % story
            self.log.info("Now processing story: %s" % url)
            response = yield from aiohttp.get(url)
            if not response.status == 200:
                text = yield from response.text()
                self.log.error("URL: %s" % url)
                self.log.error("Response status code was %s" % str(response.status))
                self.log.error(response.headers)
                self.log.error(text)
                response.close()
                continue
            json_story = yield from response.json()
            return_string.append("<%s|%s>" % (json_story['url'], json_story['title']))
        formatted_msg = "\n".join(return_string)
        return SlackAttachment(fallback=formatted_msg,
                               text=formatted_msg,
                               mrkdwn_in=["text"])

    @asyncio.coroutine
    def get_all_hn_new_stories(self):
        hn_new_stories_url = "https://hacker-news.firebaseio.com/v0/newstories.json"
        response = yield from aiohttp.get(hn_new_stories_url)
        if not response.status == 200:
            text = yield from response.text()
            self.log.error("URL: %s" % url)
            self.log.error("Response status code was %s" % str(response.status))
            self.log.error(response.headers)
            self.log.error(text)
            response.close()
            return []
        return (yield from response.json())

    def schedule_timer_message(self):
        "Print out the top five newly submitted HN stories every 5 minutes"
        timer = crontab('*/5 * * * *', func=self.send_timer_message, start=False)
        timer.start()

    @asyncio.coroutine
    def send_timer_message(self):
        raw_story_ids = yield from self.get_all_hn_new_stories()
        return_attachment = yield from self.print_top_n_hn_stories(5, raw_story_ids)
        yield from self.slack.api_call(
            'chat.postMessage',
            channel="#general",
            attachments=return_attachment,
            as_user=False,
            username="Hacker News",
            icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2016-03-18/27749445461_48.png"
        )
