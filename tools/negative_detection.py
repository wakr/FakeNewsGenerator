from textblob import TextBlob

import requests
import json


def get_ext_sentiment(new_tweet):
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

text = open("../data/whole_bbc_data.txt").read()
text = text.replace(".", " ")
output = open("../data/negative_words.txt", "w+")
words = []

for word in text.split(" "):
    blob = TextBlob(word)
    polarity = blob.sentiment.polarity
    if polarity < -0.16:
        #print(word + " " + str(polarity))
        word = word.replace(",", "")
        word = word.replace("\"", "")
        word = word.replace(".", " ")
        words.append(word)
        output.write(word + "\n")

print(words)