from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer

class Evaluator:
    def __init__(self, naive_bayes =True, evaluate_novelty = True, evaluate_value = True):
        self.naive_bayes = naive_bayes
        self.evaluate_novelty = evaluate_novelty
        self.evaluate_value = evaluate_value
        self.nb_blobber = Blobber(analyzer=NaiveBayesAnalyzer())

    def value_evaluation(self, sentence):
        blob = TextBlob(sentence)
        blob_naive_bayes = self.nb_blobber(sentence)
        polarity_tb = 1-((blob.sentiment.polarity + 1) / 2)
        polarity_nb = blob_naive_bayes.sentiment.p_neg
        print(str(polarity_tb) + " " + str(polarity_nb))
        return (polarity_nb + polarity_tb)