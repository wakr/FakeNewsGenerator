import random

from modules.preprocessing.preprocessing import Preprocessor
from modules.generation.generator import  Generator


def grab_tweet():
    path = "data/stored_tweets.txt"
    with open(path, 'r') as infile:
        tweets = infile.readlines()
    return random.choice(tweets)


def generate_text(tweet):
    pos_targets = Preprocessor(tweet).process()
    generation = Generator(*pos_targets).generate()
    return " ".join(generation)


def evaluate_text(output, tweet):
    pass


def main():
    tweet = grab_tweet()
    output = generate_text(tweet)
    result = evaluate_text(output, tweet)
    print(output)


if __name__ == '__main__':
    main()