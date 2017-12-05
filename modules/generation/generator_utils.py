
class GeneratorUtils:

    def replacement_allowed(self, word):
        not_list = ['was', 'were', 'is', 'are', 'have', 'has', 'had']
        for not_word in not_list:
            if word == not_word:
                return False
        return True