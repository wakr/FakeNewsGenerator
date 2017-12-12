import re
from textblob import TextBlob

class Preprocessor:
    def __init__(self, tweet):
        self.tweet = re.sub(r'http\:\/\/cnn.it\S+', '', tweet)  # get rid of the url

    def get_features(self, sentences):
        """
        Transform a tweet into a representation of grammar tokens of 6-tuple
        """
        print("\t-Processing tweet into sentence tuples")
        res = []
        for s in sentences:
            tags = s.tags
            get_part = lambda a, target, execptarget: [re.search(r'[^\W\d]+', w.lower()).group(0) for (w, p) in a if target in p and not execptarget in p]
            targets = s.noun_phrases
            tokens = re.findall(r'[^\W\d]+', s.raw.lower())
            nouns = get_part(tags, "NN", "NNP") # Exclude proper nouns
            verbs = get_part(tags, "VB", "*")  # verbs always start with VB
            adverbs = get_part(tags, "RB", "*")  # adverbs are closely related to adjectives
            adjectives = get_part(tags, "JJ", "*")  # true adjectives
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
