import random

from modules.preprocessing.preprocessing import Preprocessor
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


def grab_tweet():
    path = "data/stored_tweets.txt"
    with open(path, 'r') as infile:
        tweets = infile.readlines()
    return random.choice(tweets)


def generate_text(tweet):
    tokens, phrase_targets, nouns, verbs, adverbs, adjectives = Preprocessor(tweet).process()
    print(tokens)
    print("pt", phrase_targets)
    print("nouns", nouns)
    print("adj", adjectives)
    print("adverb", adverbs)
    print("verbs", verbs)
    return None


def evaluate_text(output, tweet):
    pass


def main():
    tweet = grab_tweet()
    output = generate_text(tweet)
    result = evaluate_text(output, tweet)


if __name__ == '__main__':
    main()