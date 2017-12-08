import nltk

class GeneratorUtils:

    def replacement_allowed(self, word):
        not_list = ['was', 'were', 'is', 'are', 'have', 'has', 'had']
        for not_word in not_list:
            if word == not_word:
                return False
        return True

    def get_properties(self, word):
        tags = nltk.pos_tag([word])
        tag = tags[0][1]
        properties = [] # First element will describe tense (past or not), second 3th person
        if tag == "VBN" or tag == "VBD":
            properties.append(True)
        else:
            properties.append(False)
        if not word.endswith("ss") and word.endswith("s"):
            properties.append(True)
        else:
            properties.append(False)
        if word.endswith("ing"):
            properties.append(True)
        else:
            properties.append(False)
        return properties


    def get_past(self, v):
        T, x, m = 'aeiou', "ed", v[-1]
        return [[[v + x, v + m + x][v[-2] in T and m and v[-3] not in T], [v + x, v[:-1] + "ied"][v[-2] not in T]][m == 'y'], v + "d"][m == 'e']

    def right_form(self, word, properties):
        if properties[2]:
            return word + "ing"
        if not properties[0]:  # test if in past tense
            if properties[1]: # 3th person required
                return word + "s"
            else:
                return word
        else:
            return self.get_past(word)