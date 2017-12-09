import os
import random
import re
import sys

from modules.preprocessing.preprocessing import Preprocessor
from modules.generation.generator import Generator
from modules.evaluator import Evaluator
from modules.tweet_grabber import collect_tweets

from itertools import product


def grab_tweet():
    tweet_file = "data/stored_tweets.txt"

    # Check if there is file with tweets available
    if not os.path.isfile(tweet_file):
        # If not collect some
        tweets = collect_tweets('CNN', 10)
        with open(tweet_file, 'w') as outfile:
            outfile.write('\n'.join(tweets))
    else:
        # Else read existing tweets
        with open(tweet_file, 'r') as infile:
            tweets = infile.readlines()

    # Select one tweet for processing
    selected_tweet = random.choice(tweets)
    # Remove new line, if present
    selected_tweet = selected_tweet.replace('\n','')
    # Remove possible hyperlink
    return re.sub(r'http\:\/\/cnn.it\S+', '', selected_tweet)


def generate_text(tweet):
    pos_targets = Preprocessor(tweet).process()
    generation = Generator(pos_targets).generate()
    print("\t-Starting to form combinations...")
    generation_combinations = list(product(*generation))
    print("\t-Formed {} different combinations".format(len(generation_combinations)))
    res = ""
    for sent_cands in generation_combinations:
        res += ". ".join(sent_cands) + "\n"
    # Perform internal evaluation although it does not presently affect anything
    # save that it takes a fixed size of samples from generated
    sampled = internal_evaluation(res, tweet)
    final_res = external_evaluation(sampled)
    return final_res

def external_evaluation(top_candidates):
    use_quota = False  # change to True only when all other blocks of this software is done
    if not use_quota:
        return top_candidates
    print("\t-Starting external evaluation for {} candidate Tweets".format(len(top_candidates)))
    lcleval = Evaluator()
    scored_top = [(t, lcleval.external_evaluation(t)) for (t, s) in top_candidates]
    scored_top = sorted(scored_top, key=lambda x: x[1], reverse=True)
    return scored_top[0]  # the best

def internal_evaluation(generated, original_tweet):
    print("\t-Starting internal evaluation")
    lcleval = Evaluator()
    # Evaluate original tweet
    org_eval = lcleval.value_evaluation_for_words(original_tweet)

    # Split generated tweets to a list
    tweets = generated.split('\n')[:-1]  # remove the last \n

    # Collect list of generated tweets that score higher than original
    rtweets = []
    for atweet in tweets:
        res = lcleval.value_evaluation_for_words(atweet)
        novelty = lcleval.novelty_evaluation(atweet)
        score = (-res) + novelty  # The lower the score, the better
        if res > org_eval:
            rtweets.append((atweet, score))
    print("\t-Evaluation done")
    # Sort collected tweets in order based on their score
    rtweets = sorted(rtweets, key=lambda x: x[1], reverse=True)
    # Select sample of them
    sampled = rtweets[:10] # take max top-10
    return sampled



def main():
    tweet = grab_tweet()
    print(tweet)
    output = generate_text(tweet)
    # Display generated texts
    for t, s in output:
        print(t)


if __name__ == '__main__':
    main()
