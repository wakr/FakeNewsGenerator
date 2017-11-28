from textblob import TextBlob

text = open("../whole_bbc_data.txt").read()
text = text.replace(".", " ")
output = open("negative_words.txt", "w+")
words = []

for word in text.split(" "):
    blob = TextBlob(word)
    polarity = blob.sentiment.polarity
    if polarity < 0:
        word = word.replace(",", "")
        word = word.replace("\"", "")
        word = word.replace(".", " ")
        words.append(word)
        output.write(word + "\n")

print(words)