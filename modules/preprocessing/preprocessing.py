from textblob import TextBlob

import re

class Preprocessor:
    def __init__(self, tweet):
        self.tweet = re.sub(r'http\:\/\/cnn.it\S+', '', tweet)

    def process(self):
        """
        Transform a tweet into a representation of grammar tokens of 6-tuple
        """
        get_part = lambda a, target: [w.lower() for (w, p) in a if target in p]
        blob = TextBlob(self.tweet)
        tags = blob.tags
        targets = blob.noun_phrases
        proper_nouns = get_part(tags, "NN")
        verbs = get_part(tags, "VB")  # verbs always start with VB
        adverbs = get_part(tags, "RB")  # adverbs are closely related to adjectives
        adjectives = get_part(tags, "JJ")  # true adjectives
        return list(blob.tokens.lower()), list(targets), proper_nouns, verbs, adverbs, adjectives
