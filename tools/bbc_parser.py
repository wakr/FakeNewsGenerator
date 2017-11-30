import glob
import os

result = open("../data/whole_bbc_data.txt", "w+")

for filename in glob.iglob('**/*.txt', recursive=True):
     print(filename)
     file = open(filename, "r")
     text = file.read()
     text = os.linesep.join([s for s in text.splitlines() if s])
     result.write(text)
