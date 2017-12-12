import nltk

class GeneratorUtils:

    def replacement_allowed(self, word):
        """
        Return true if replacement of word is allowed, false if not allowed. List of specific words is not allowed for replacement.
        :param word:
        :return: boolean
        """
        not_list = ['was', 'were', 'is', 'are', 'have', 'has', 'had', 'be']
        for not_word in not_list:
            if word == not_word:
                return False
        return True

    def get_properties_adjective(self, word):
        """
        Get properties of adjective to list of booleans. Checks er and est endings.
        :param word: string
        :return: property list, list of booleans
        """
        properties = []
        if word.endswith("est"):
            properties.append(True)
        else:
            properties.append(False)
        if word.endswith("er"):
            properties.append(True)
        else:
            properties.append(False)
        return properties

    def right_form_adjective(self, word, properties):
        """
        Returns the replacement word in right form based on the properties of the original word.
        :param word: string
        :param properties: list of booleans
        :return:
        """
        if properties[0]:
            if word.endswith("e"):
                return word + "st"
            else:
                return word + "est"
        if properties[1]:
            if word.endswith("e"):
                return word + "r"
            else:
                return word + "er"
        return word


    def get_properties_verb(self, word):
        """
        Get properties of verb. Checks the past tense, 3th person and ing -form
        :param word:
        :return: list of properties, list of booleans
        """
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
        """
        Get past form of verb, works for regular verbs
        :param v: verb
        :return: string, past tense of verb
        """
        T, x, m = 'aeiou', "ed", v[-1]
        return [[[v + x, v + m + x][v[-2] in T and m and v[-3] not in T], [v + x, v[:-1] + "ied"][v[-2] not in T]][m == 'y'], v + "d"][m == 'e']

    def right_form_verb(self, word, properties):
        """
        Get replacement verb in right form based on properties list
        :param word: string
        :param properties:  list of booleans
        :return:  verb in right form
        """
        if properties[2]:
            return word + "ing"
        if not properties[0]:  # test if in past tense
            if properties[1]: # 3th person required
                return word + "s"
            else:
                return word
        else:
            return self.get_past(word)