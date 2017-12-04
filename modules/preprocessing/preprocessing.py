from textblob import TextBlob
import nltk
import re


class Preprocessor:
    def __init__(self, tweet):
        self.tweet = re.sub(r'http\:\/\/cnn.it\S+', '', tweet)  # get rid of the url

    def get_features(self, sentences):
        """
        Transform a tweet into a representation of grammar tokens of 6-tuple
        """
        res = []
        for s in sentences:
            tags = s.tags
            get_part = lambda a, target: [w.lower() for (w, p) in a if target in p]
            targets = s.noun_phrases
            tokens = re.findall(r'[^\W\d]+', s.raw.lower())
            proper_nouns = get_part(tags, "NN")
            verbs = get_part(tags, "VB")  # verbs always start with VB
            adverbs = get_part(tags, "RB")  # adverbs are closely related to adjectives
            adjectives = get_part(tags, "JJ")  # true adjectives
            feature_map = {"tokens": tokens,
                           "phrase_targets": list(targets),
                           "nouns": proper_nouns,
                           "verbs": verbs,
                           "adverbs": adverbs,
                           "adjectives": adjectives}
            res.append(feature_map)
        return res

    def process(self):
        """
        :return: Array of features extracted from text
        """
        blob = TextBlob(self.tweet)
        sents = blob.sentences
        return self.get_features(sents)
