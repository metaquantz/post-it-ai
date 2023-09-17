"""Config init"""
import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        """Init os environ config as object"""
        load_dotenv()
        self.__dict__.update(os.environ)

    def get_config(self):
        """Return config object"""
        return self.__dict__
