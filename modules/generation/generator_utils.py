import nltk

class GeneratorUtils:

    def replacement_allowed(self, word):
        not_list = ['was', 'were', 'is', 'are', 'have', 'has', 'had']
        for not_word in not_list:
            if word == not_word:
                return False
        return True

    def is_past_tense(self, word):
        tags = nltk.pos_tag([word])
        tag = tags[0][1]
        if tag == "VBN" or tag == "VBD":
            return True
        else:
            return False


    def get_past(self, v):
        T, x, m = 'aeiou', "ed", v[-1]
        return [[[v + x, v + m + x][v[-2] in T and m and v[-3] not in T], [v + x, v[:-1] + "ied"][v[-2] not in T]][m == 'y'], v + "d"][m == 'e']

    def right_form(self, word, past_tense):
        if not past_tense:
            return word
        else:
            return self.get_past(word)