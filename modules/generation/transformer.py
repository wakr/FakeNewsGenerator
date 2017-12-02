import json, requests


def explore_space(word):
    """
    Explores the thesaurus for anto/synonymes
    :param word:
    :return: dictionary where all similarities and POS's are represented. Empty array for non-existent
    """
    api_key = "e3e5ce1ed471cf79c5415984ab2874f1"
    wordapi_url = "http://words.bighugelabs.com/api/2/{}/{}/json".format(api_key, word)
    res = requests.get(wordapi_url)
    data = json.loads(res.text)

    possible_POS = ["adjective", "noun", "verb", "adverb"]
    possible_similarities = ["ant", "sim", "syn", "rel", "usr"]

    space = {}
    for p in possible_POS:
        space[p] = {}
        if p in data.keys():
            for s in possible_similarities:
                if s in data[p].keys():
                    space[p][s] = data[p][s]
                else:
                    space[p][s] = []
        else:
            for s in possible_similarities:
                space[p][s] = []
    return space

def generate_neg_adjectives(adjs):
    pass

def generate_neg_nouns(nouns):
    pass

def retarget_word(noun_phrases):
    pass