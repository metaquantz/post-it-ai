# Post-it-ai

import logging
import json
from newsapi import NewsApiClient
from post_it_ai.lib.openai_chat import OpenAIChat
from post_it_ai.util.get_config import Config


class PostItAI:
    """Post IT AI Class"""

    def __init__(self):
        """Init class"""
        logging.basicConfig(encoding="utf-8", level=logging.INFO)
        self.logger = logging.getLogger("Post-IT-AI")
        self.cfg = Config().get_config()
        self.newsapi = NewsApiClient(api_key=self.cfg.get("NEWSAPI_KEY"))
        # self.open_ai_chat = OpenAIChat(model=self.cfg.get("CHAT_GPT_MODEL"))

    def run_app(self, news_query=None):
        """Run app"""
        if not news_query:
            self.logger.error("No query given")
            exit(1)
        self.logger.info("Running Post IT AI for query {}".format(news_query))

        news_articles = self.newsapi.get_everything(
            q=news_query, language="en", sort_by="relevancy"
        )

        json_result = json.dumps(news_articles, sort_keys=True, indent=4)

        with open("news_articles_{}.json".format(news_query), "w") as f:
            f.write(json_result)

        self.logger.info("News API Results: {}".format(json_result))

        with open("sources.json", "w") as f:
            f.write(json.dumps(self.newsapi.get_sources(), sort_keys=True, indent=4))
