from textblob import TextBlob

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
