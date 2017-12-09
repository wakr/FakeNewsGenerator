import os
import random
import re
import sys

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
    tb = TextBlob(tweet)
    sent_gens = {}
    # Split original tweet into sentences
    for sentence_nr, sentence in enumerate(tb.sentences):
        # Preprocess sentence
        pos_targets = Preprocessor(str(sentence)).process()
        # Generate alternatives for it
        generation = Generator(pos_targets).generate()
        print("\t-Starting to form combinations...")
        generation_combinations = list(product(*generation))
        print("\t-Formed {} different combinations".format(len(generation_combinations)))
        res = ""
        for sent_cands in generation_combinations:
            res += ". ".join(sent_cands) + "\n"
        # If res is empty generator failed to produce any output
        if not res:
            print('Generation has failed')
        # Perform internal evaluation although it does not presently affect anything
        # save that it takes a fixed size of samples from generated
        sampled = internal_evaluation(res, str(sentence))
        # Add original sentence and its variants for tweet reconstruction
        # List index is sentence place in tweet and tuple contains original sentence
        # plus its generated sentences
        sampled = [sample[0] for sample in sampled]
        sent_gens[sentence_nr] = (str(sentence), sampled)

    gen_samples = []
    # Recostruct new tweets from generated results
    # NOTE: At this point reconstructing maps only one generated sentence to another
    #       one and does not do all permutations. So if you had two sentences A and B
    #       that produce A1, A2, B1 and B2 then output is A1 B1 and A2 B2.
    print('\t-Reconstructing tweets')
    for idx in range(len(sent_gens.keys())):
        # Original sentence from tweet
        sentence = sent_gens[idx][0]
        # Its generated variants
        generated_sentences = sent_gens[idx][1]
        # Check that there were some results
        if generated_sentences:
            # Reconstruct new tweet sentence from original and generated
            for sample_idx, generated in enumerate(generated_sentences):
                # In case there were more generated possibilities in later sentences
                # than the earlier ones this skips them
                if idx > 0 and sample_idx > len(gen_samples) - 1: continue
                sample = regenerate_tweet(sentence, generated)
                # Append further sentences to new tweet, if any
                if idx > 0:
                    gen_samples[sample_idx] += ' ' + sample
                else:
                    gen_samples.append(sample)
                # In some cases generation might produce fewer variants to later
                # sentences and this just appends one currently used to others.
                if len(generated_sentences) < len(gen_samples):
                    for dup_idx in range(sample_idx + 1, len(gen_samples)):
                        gen_samples[dup_idx] += ' ' + sample
        else:
            # If evaluation has not accepted any choices use the original sentence
            print('Evaluation has failed')
            gen_samples.append(sentence)

    final_res = external_evaluation(gen_samples)

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
            end_punct = None
        # Similarly handle words that begin with certain punctuation
        if re.search(r'^[\"\']', word) is not None:
            start_punct = word[0]
            word = word[1:]
        else:
            start_punct = None

        # If original word begins with @ then use it. Position remains same as generator
        # has only removed @
        if re.search(r'^[@]+', word):
            result.append(word)
            continue

        # If original word contains certain punctution use original instead
        # and increase adder to use one word beyond on the generated text. This
        # handles e.g. "'s" "'d" cases
        if re.search(r"[-\'\"]+", word) is not None:
            adder += 1
            result.append(word)
            continue

        # Check if original word needs to be replaced with generated word
        if word.lower() != top_generated_lst[idx + adder]:
            use_word = top_generated_lst[idx + adder]
        else:
            # If not use the original word
            use_word = word

        # Add earlier removed punctuation, if any
        if start_punct:
            use_word = start_punct + use_word
        if end_punct:
            use_word += end_punct
        result.append(use_word)

    new_sentence = ' '.join(result)

    return new_sentence

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
    rtweets = sorted(rtweets, key=lambda x: x[1], reverse=False)
    # Select sample of them
    sampled = rtweets[:10] # take max top-10
    return sampled


def main():
    tweet = grab_tweet()
    print(tweet)
    output = generate_text(tweet)
    # Display generated texts
    for t in output:
        print(t)


if __name__ == '__main__':
    main()
