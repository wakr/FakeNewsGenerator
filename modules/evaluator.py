import json
import os
import requests

from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from gensim.models import Word2Vec

class Evaluator:
    ''' Evaluation related functionalities. '''

    def __init__(self):
        """
        Initialization of evaluator
        """
        self.nb_blobber = Blobber(analyzer=NaiveBayesAnalyzer())
        curr_dir = os.path.dirname(__file__)
        # In our novelty evaluation we are using Word2Vec model trained with Reuters news titles
        self.model = Word2Vec.load(os.path.join(curr_dir, "../data/Model"))
        self.read_negative_words()
        self.word_negativities = {}


    def read_negative_words(self):
        """ Read negative word list for evaluation. """
        curr_dir = os.path.dirname(__file__)
        filename = os.path.join(curr_dir, '../data/negative_word_list.txt')
        text = open(filename).read()
        self.negative_words = set(text.split("\n"))


    def novelty_evaluation(self, text):
        """ Evaluate text novelty.

            Lower score, better novelty.
        """
        score = self.model.score([text])
        repetitiveness = max(TextBlob(text).word_counts.values())
        return score[0] * repetitiveness

    def external_evaluation(self, text):
        """ Evaluate final generated tweet.

        This is used for evaluating the final tweet. It's novelty and negativity
        value combined, first scaling novelty. Higher value is better.
        """
        nov = -1*(self.novelty_evaluation(text))/1000
        val = self.get_final_evaluation(text)['neg']
        return nov + val

    def value_evaluation(self, word):
        """ Evaluate word negativity.

        Higher value is better.
        """
        sum = 0
        if word in self.negative_words:
            sum += 0.5
        blob = TextBlob(word)
        blob_naive_bayes = self.nb_blobber(word)
        polarity_tb = 1-((blob.sentiment.polarity + 1) / 2)
        polarity_nb = blob_naive_bayes.sentiment.p_neg
        return sum + polarity_nb + polarity_tb

    def value_evaluation_for_words(self, sentence):
        """ Evaluate sentence negativity. """
        sum = 0
        blob = self.nb_blobber(sentence)
        for word in blob.words:
            # Too often occurring word that irritates one group member
            if word.startswith("retard"):
                sum += -10
                continue
            if word in self.word_negativities:
                sum += self.word_negativities[word]
            else:
                neg = self.value_evaluation(word)
                sum += neg
                self.word_negativities[word] = neg
        return sum

    def get_final_evaluation(self, new_tweet):
        """ Final evaluator for generated tweet.

        Function evaluates negativity of sentence using Sentity.
        The final evaluation of tweet. Note 25000 limit per month!

        :param new_tweet: phenotype
        :return dictionary with pos/neg scores
        """
        api_key = "token b4873f0f50aa5e871dbf830cd53754051ef9dc73"
        base_url = "https://api.sentity.io/v1/sentiment?text={}".format(new_tweet)
        headers = {'Authorization': api_key}
        resp = requests.get(url=base_url, headers=headers)
        data = json.loads(resp.text)
        return data
