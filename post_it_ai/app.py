# Post-it-ai

import logging
import json
from newscatcherapi import NewsCatcherApiClient
from lib.openai_chat import OpenAIChat
from util.get_config import Config
from util.response import API_RESPONSE


class PostItAI:
    """Post IT AI Class"""

    def __init__(self):
        """Init class"""
        logging.basicConfig(encoding='utf-8', level=logging.INFO)
        self.logger = logging.getLogger("Post-IT-AI")
        self.cfg = Config().get_config()
        self.newsapi = NewsCatcherApiClient(x_api_key=self.cfg.get("NEWSCATCHER_API_KEY"))
        self.open_ai_chat = OpenAIChat(model=self.cfg.get("CHAT_GPT_MODEL"))

    def run_app(self, news_query=None):
        """Run app"""
        if not news_query:
            self.logger.error("No query given")
            exit(1)
        self.logger.info("Running Post IT AI for query {}".format(news_query))

        # news_articles = newscatcherapi.get_search(q="Tesla")

        news_articles = API_RESPONSE

        json_result = json.dumps(news_articles, sort_keys=True, indent=4)

        self.logger.info("News API Results: {}".format(json_result))
