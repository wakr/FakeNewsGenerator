from textblob import TextBlob

import requests
import json


class WordNet:
    """
    Make api-calls to gain more knowledge about words
    """
    def __init__(self):
        self.datamuse_base_url = "https://api.datamuse.com/words?rel_jjb="