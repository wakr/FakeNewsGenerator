import json, requests

wordapi_url = "https://wordsapiv1.p.mashape.com/words/"


def find_antonymes_for_adjective(adj):
    query_url = "{}/antonyms".format(adj)
    res = requests.get(wordapi_url + query_url)
    print(res)







find_antonymes_for_adjective("fast")