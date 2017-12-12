from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from gensim.models import Word2Vec
from nltk import tokenize

import requests
import json
import os


class Evaluator:
    def __init__(self):
        """
        Initialization of Evaluator
        """
        self.nb_blobber = Blobber(analyzer=NaiveBayesAnalyzer())
        dir = os.path.dirname(__file__)
        self.model = Word2Vec.load(os.path.join(dir, "../data/Model")) # In our novelty evaluation we are using Word2Vec model trained with reuters news titles
        self.read_negative_words()
        self.word_negativities = {}


    def read_negative_words(self):
        """ We are using negative words list in evaluating value of word. This function reads the negative words list """
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../data/negative_word_list.txt')
        text = open(filename).read()
        self.negative_words = set(text.split("\n"))


    def novelty_evaluation(self, text):
        """ Novelty evaluation is log propability of text occurring according to our Word2Vec model. Lower score, better novelty.
        :rtype: object
        """
        score = self.model.score([text])
        repetitiveness = max(TextBlob(text).word_counts.values())
        return score[0] * repetitiveness

    def external_evaluation(self, text):
        """
        External evaluation is used for evaluating the final tweet. It's novelty and negativity value combined, first scaling novelty.
        Higher, better.
        :param text:
        :return:
        """
        nov = -1*(self.novelty_evaluation(text))/1000
        val = self.get_final_evaluation(text)['neg']
        return nov + val

    def value_evaluation(self, sentence):
        """
        Value evaluation is weighted sum which is not between 0, 1. It evaluates negativity. Higher, better.
        :param sentence: preprocessed sentence or single word
        :return: negativity
        """
        sum = 0
        if sentence in self.negative_words:
            sum += 0.5
        blob = TextBlob(sentence)
        blob_naive_bayes = self.nb_blobber(sentence)
        polarity_tb = 1-((blob.sentiment.polarity + 1) / 2)
        polarity_nb = blob_naive_bayes.sentiment.p_neg
        return sum + polarity_nb + polarity_tb

    def value_evaluation_for_words(self, sentence):
        """
        Value (negativity) evaluation for whole sentence
        :param sentence:  string
        :return: sum of negativities of words in sentence
        """
        sum = 0
        blob = self.nb_blobber(sentence)
        for word in blob.words:
            if word.startswith("retard"):
                sum += -1000
                continue
            if word in self.word_negativities:
                sum += self.word_negativities[word]
            else:
                neg = self.value_evaluation(word)
                sum += neg
                self.word_negativities[word] = neg
        return sum




    def get_final_evaluation(self, new_tweet):
        """
        This function evaluates negativity of sentence using WordNet.
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
