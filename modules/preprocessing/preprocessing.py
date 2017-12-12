import re
from textblob import TextBlob

class Preprocessor:
    def __init__(self, tweet):
        self.tweet = re.sub(r'http\:\/\/cnn.it\S+', '', tweet)  # get rid of the url

    def get_part(self, a, target, execptarget):
        res = []
        for (w, p) in a:
            if target in p and not execptarget in p:
                words = re.search(r'[^\W\d]+', w.lower())
                if not words:
                    res.append(w)
                else:
                    res.append(words.group(0))
        return res

    def get_features(self, sentences):
        """
        Transform a tweet into a representation of grammar tokens of 6-tuple
        """
        print("\t-Processing tweet into sentence tuples")
        res = []
        for s in sentences:
            tags = s.tags
            targets = s.noun_phrases
            tokens = re.findall(r'[^\W\d]+', s.raw.lower())
            nouns = self.get_part(tags, "NN", "NNP") # Exclude proper nouns
            verbs = self.get_part(tags, "VB", "*")  # verbs always start with VB
            adverbs = self.get_part(tags, "RB", "*")  # adverbs are closely related to adjectives
            adjectives = self.get_part(tags, "JJ", "*")  # true adjectives
            feature_map = {"tokens": tokens,
                           "phrase_targets": list(targets),
                           "nouns": nouns,
                           "verbs": verbs,
                           "adverbs": adverbs,
                           "adjectives": adjectives}
            res.append(feature_map)
        print("\t-Processing done")
        return res

    def process(self):
        """
        :return: Array of features extracted from text
        """
        blob = TextBlob(self.tweet)
        sents = blob.sentences
        return self.get_features(sents)
