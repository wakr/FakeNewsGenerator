from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from gensim.models import Word2Vec

class Evaluator:
    def __init__(self, evaluate_novelty = True, evaluate_value = True):
        self.evaluate_novelty = evaluate_novelty
        self.evaluate_value = evaluate_value
        self.nb_blobber = Blobber(analyzer=NaiveBayesAnalyzer())
        self.model = Word2Vec.load("../data/Model")
        self.read_negative_words()

    def read_negative_words(self):
        text = open("../data/negative_word_list.txt").read()
        self.negative_words = set(text.split("\n"))
        print(self.negative_words)

    def novelty_evaluation(self, text):
        score = self.model.score([text])
        return score


    def value_evaluation(self, sentence):
        if sentence in self.negative_words:
            return 2.0
        blob = TextBlob(sentence)
        blob_naive_bayes = self.nb_blobber(sentence)
        polarity_tb = 1-((blob.sentiment.polarity + 1) / 2)
        polarity_nb = blob_naive_bayes.sentiment.p_neg
        print(str(polarity_tb) + " " + str(polarity_nb))
        return (polarity_nb + polarity_tb)