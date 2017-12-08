from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from gensim.models import Word2Vec
from nltk import tokenize

import requests
import json
import os


class Evaluator:
    def __init__(self, evaluate_novelty = True, evaluate_value = True):
        self.evaluate_novelty = evaluate_novelty
        self.evaluate_value = evaluate_value
        self.nb_blobber = Blobber(analyzer=NaiveBayesAnalyzer())
        #self.model = Word2Vec.load("../data/Model")
        self.read_negative_words()

    def read_negative_words(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../data/negative_word_list.txt')
        text = open(filename).read()
        self.negative_words = set(text.split("\n"))

    def novelty_evaluation(self, text):
        score = self.model.score([text])
        return score

    # Value evaliation is weighted sum which is not between 0, 1
    def value_evaluation(self, sentence):
        sum = 0
        if sentence in self.negative_words:
            sum += 1
        blob = TextBlob(sentence)
        blob_naive_bayes = self.nb_blobber(sentence)
        polarity_tb = 1-((blob.sentiment.polarity + 1) / 2)
        polarity_nb = blob_naive_bayes.sentiment.p_neg
        return sum + polarity_nb + polarity_tb

    def value_evaluation_for_words(self, sentence):
        sum = 0
        blob = self.nb_blobber(sentence)
        for word in blob.words:
            sum += self.value_evaluation(word)
        return sum



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
