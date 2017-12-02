import gensim
from gensim.models import Word2Vec
# Reuters.txt should be txt file in one sentence per line

text = open("../data/reuters.txt").read().split("\n")

sentences = []
for sen in text:
    sentences.append(sen.split(" "))

model = gensim.models.Word2Vec(sentences, min_count=1, hs=1, negative=0)
model.save("../data/Model")

