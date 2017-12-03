from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from gensim.models import Word2Vec

import requests
import json


class Evaluator:
    def __init__(self, evaluate_novelty = True, evaluate_value = True):
        self.evaluate_novelty = evaluate_novelty
        self.evaluate_value = evaluate_value
        self.nb_blobber = Blobber(analyzer=NaiveBayesAnalyzer())
        self.model = Word2Vec.load("../data/Model")

    def novelty_evaluation(self, text):
        score = self.model.score([text])
        return score

    def value_evaluation(self, sentence):
        blob = TextBlob(sentence)
        blob_naive_bayes = self.nb_blobber(sentence)
        polarity_tb = 1-((blob.sentiment.polarity + 1) / 2)
        polarity_nb = blob_naive_bayes.sentiment.p_neg
        print(str(polarity_tb) + " " + str(polarity_nb))
        return polarity_nb + polarity_tb

    def get_final_evaluation(new_tweet):
        """
        The final evaluation of tweet. Note 25000 limit per month :(
        :param new_tweet: phenotype
        :return dictionary with pos/neg scores
        """
        api_key = "token b4873f0f50aa5e871dbf830cd53754051ef9dc73"
        base_url = "https://api.sentity.io/v1/sentiment?text={}".format(new_tweet)
        headers = {'Authorization': api_key}
        resp = requests.get(url=base_url, headers=headers)
        data = json.loads(resp.text)
        return data
