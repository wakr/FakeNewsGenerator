import os
import random
import re

from itertools import product
from textblob import TextBlob

from modules.preprocessing.preprocessing import Preprocessor
from modules.generation.generator import Generator
from modules.evaluator import Evaluator
from modules.tweet_grabber import collect_tweets

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

    # Remove empty lines, if any
    tweets = [tweet.strip() for tweet in tweets if len(tweet.strip()) > 1]
    # Select one tweet for processing
    selected_tweet = random.choice(tweets)
    # Remove new line, if present
    selected_tweet = selected_tweet.replace('\n', '')
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

def regenerate_tweet(tweet_sentence, generated_sentence):
    '''Re-generate tweet based on generated results'''
    result = []
    tweet_sentence_lst = tweet_sentence.split()
    top_generated_lst = generated_sentence.split()
    # Adder is used to reposition what word is used in generated tweet
    adder = 0
    # Reconstruct twet word by word
    for idx, word in enumerate(tweet_sentence_lst):
        # If original contains numbers, e.g. "32", or it contains only some punctuations,
        # e.g. '--', then the generator has eliminated these words and we use original
        # word but have to reduce adder by one to compensate what to use next word
        # in generated sentence
        if (re.search(r'[0-9]+', word) is not None) or \
            (re.search(r"[-\'\"]+", word) is not None and re.search(r'[A-Za-z]',word) is None):
            adder -= 1
            result.append(word)
            continue

        # If original word contains certain punctuation at the end, remove it and store
        # for later re-attachment
        if re.search(r'[.,!\?\"]$', word) is not None:
            end_punct = word[-1]
            word = word[:-1]
        else:
            end_punct = ''
        # Similarly handle words that begin with certain punctuation
        if re.search(r'^[\"\']', word) is not None:
            start_punct = word[0]
            word = word[1:]
        else:
            start_punct = ''

        # If original word begins with @ then use it. Position remains same as generator
        # has only removed @
        if re.search(r'^[@]+', word) or re.search(r'[\"]+', word):
            result.append(word)
            continue

        # If original word contains certain punctution use original instead
        # and increase adder to use one word beyond on the generated text. This
        # handles e.g. "'s" "'d" cases
        if re.search(r"[-\']+", word) is not None:
            adder += 1
            result.append(start_punct + word + end_punct)
            continue

        # Check if original word needs to be replaced with generated word
        if word.lower() != top_generated_lst[idx + adder]:
            if top_generated_lst[idx + adder].endswith('.'):
                use_word = top_generated_lst[idx + adder][:-1]
            else:
                use_word = top_generated_lst[idx + adder]
        else:
            # If not use the original word
            use_word = word

        result.append(start_punct + use_word + end_punct)

    new_sentence = ' '.join(result)

    return new_sentence

def update_progress(amtDone):
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(amtDone * 50), amtDone * 100), end="")

def external_evaluation(top_candidates):
    use_quota = False  # change to True only when all other blocks of this software is done
    if not use_quota:
        return top_candidates[0]
    print("\t-Starting external evaluation for {} candidate Tweets".format(len(top_candidates)))
    lcleval = Evaluator()
    scored_top = [(t, lcleval.external_evaluation(t)) for (t, s) in top_candidates]
    scored_top = sorted(scored_top, key=lambda x: x[1], reverse=True)
    return scored_top[0]  # the best

def internal_evaluation(generated, original_tweet):
    print("\t-Starting internal evaluation")
    lcleval = Evaluator()
    # Evaluate original tweet
    org_res = lcleval.value_evaluation_for_words(original_tweet)

    # Split generated tweets to a list
    tweets = generated.split('\n')[:-1]  # remove the last \n

    # Collect list of generated tweets that score higher than original
    rtweets = []
    i = 0
    for atweet in tweets:
        res = lcleval.value_evaluation_for_words(atweet)
        novelty = lcleval.novelty_evaluation(atweet)
        score = (-res) + novelty  # The lower the score, the better
        if res > org_res:
            rtweets.append((atweet, score))
        i += 1
        update_progress(round(i / len(tweets), 1))
    print("\n\t-Evaluation done")
    # Sort collected tweets in order based on their score
    rtweets = sorted(rtweets, key=lambda x: x[1], reverse=False)
    # Select sample of them
    sampled = rtweets[:10]  # take max top-10
    return sampled


def format_output(original_tweet, generated_tweet):
    tb1 = TextBlob(original_tweet).sentences
    tb2 = TextBlob(generated_tweet).sentences
    joined = " ".join([regenerate_tweet(str(os), str(gs)) for (os, gs)in zip(tb1, tb2)])
    return joined.replace("_", " ")


def main():
    tweet = grab_tweet()
    print(tweet)
    output = generate_text(tweet)
    # Display generated texts
    formatted_output = format_output(tweet, output[0])
    print(formatted_output)


if __name__ == '__main__':
    main()
