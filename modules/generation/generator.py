from modules.evaluator import Evaluator
from textblob import Word
from textblob.wordnet import ADJ, VERB, NOUN
from modules.generation.generator_utils import GeneratorUtils


class Generator:
    def __init__(self, pos_sentences):
        self.pos_sentences = pos_sentences
        self.evaluator = Evaluator()
        self.generator_utils = GeneratorUtils()

    def replace_candidates_to_original(self, target, verbs_c, adjectives_c, nouns_c, max_recursion, current=0):
        """
        Recursively replaces POS-candidates to original tweet. Takes only one sentence at a time
        :param target: the tokens of original tweet
        :param verbs_c: dict of verb candidates
        :param adjectives_c: dict of adjective candidates
        :param nouns_c: dict of noun candidates
        :param max_recursion: maximum recursion depth to early cut off
        :param current: current recursion depth
        :return: lists of candidate tweets
        """
        generations = []
        if current == max_recursion:
            return generations
        for v in verbs_c.keys():
            if not v in target["tokens"]:  # original already reassigned
                continue
            for candidate in verbs_c[v]:
                temp_tokens = list(target["tokens"])
                for (i, t) in enumerate(temp_tokens):
                    if t == v:  # hot-fix to deal with e.g s and 's (here's)
                        temp_tokens[i] = candidate[0]  # tuple (word, score)
                        generations.append(temp_tokens)

        for a in adjectives_c.keys():
            if not a in target["tokens"]:  # original already reassigned
                continue
            for candidate in adjectives_c[a]:
                temp_tokens = list(target["tokens"])
                for (i, t) in enumerate(temp_tokens):
                    if t == a:
                        temp_tokens[i] = candidate[0]  # tuple (word, score)
                        generations.append(temp_tokens)

        for n in nouns_c.keys():
            if not n in target["tokens"]:  # original already reassigned
                continue
            for candidate in nouns_c[n]:
                temp_tokens = list(target["tokens"])
                for (i, t) in enumerate(temp_tokens):
                    if t == n:
                        temp_tokens[i] = candidate[0]  # tuple (word, score)
                        generations.append(temp_tokens)
        res = list(generations)
        for g in generations:
            rec = self.replace_candidates_to_original({"tokens": g}, verbs_c, adjectives_c, nouns_c, max_recursion, current + 1)
            res.append(rec)
        return res

    def get_n_highest(self, candidate_scores, n=1):
        """
        Gets n-highest candidates for POS-class
        :param candidate_scores: scores per candidates
        :param n: how many to take from sorted list
        :return: dict of best candidates
        """
        res = {}
        for k in candidate_scores.keys():
            cands = candidate_scores[k]
            top_n = sorted(cands, key=lambda x: x[1], reverse=True)[:n]
            res[k] = top_n
        return res

    def replacement_allowed(self, word):
        """
        Prevent replacing specific words
        :param word: candidate
        :return: is replacement allowed
        """
        not_list = ['was', 'were', 'is', 'are', 'have', 'has', 'had']
        for not_word in not_list:
            if word == not_word:
                return False
        return True

    def negatize_verbs(self, sent_target, max_synset_len=3):
        """
        Looks for negative verb candidates
        :param sent_target: target verbs
        :param max_synset_len: maximum allowed wideness
        :return: verb candidates
        """
        candidates = {}
        flatten = lambda l: [item for sublist in l for item in sublist]
        for w in sent_target["verbs"]:
            candidates[w] = [(w, self.evaluator.value_evaluation(w))]
            properties = self.generator_utils.get_properties_verb(w)
            if not self.generator_utils.replacement_allowed(w):
                continue
            synsets = Word(w).get_synsets(pos=VERB)[:max_synset_len]
            upper_meanings = []
            for ss in synsets:
                hype = flatten([h.lemmas() for h in ss.hypernyms()])
                hypo = flatten([h.lemmas() for h in ss.hyponyms()])
                upper_meanings += hype
                upper_meanings += hypo
                upper_meanings += flatten([u.antonyms() for u in upper_meanings])  # find all candidate antonyms
                upper_meanings = list(set(upper_meanings))
            for l in upper_meanings:
                val = self.evaluator.value_evaluation(l.name().lower())
                candidates[w].append((self.generator_utils.right_form_verb(l.name().lower(), properties), val))
        return candidates

    def negatize_nouns(self, sent_target, max_synset_len=3):
        """
        Looks for negative noun candidates
        :param sent_target: target nouns
        :param max_synset_len: maximum allowed wideness
        :return: noun candidates
        """
        candidates = {}
        flatten = lambda l: [item for sublist in l for item in sublist]
        for w in sent_target["nouns"]:
            candidates[w] = [(w, self.evaluator.value_evaluation(w))]
            synsets = Word(w).get_synsets(pos=NOUN)[:max_synset_len]
            upper_meanings = []
            for ss in synsets:
                hype = flatten([h.lemmas() for h in ss.hypernyms()])
                hypo = flatten([h.lemmas() for h in ss.hyponyms()])
                upper_meanings += hype
                upper_meanings += hypo
                upper_meanings += flatten([u.antonyms() for u in upper_meanings])
                upper_meanings = list(set(upper_meanings))
            for l in upper_meanings:
                val = self.evaluator.value_evaluation(l.name().lower())
                candidates[w].append((l.name().lower(), val))
        return candidates

    def negatize_adjectives(self, sent_target, max_synset_len=3):
        """
        Looks for negative adjective candidates
        :param sent_target: target adjectives
        :param max_synset_len: maximum allowed wideness
        :return: adjective candidates
        """
        candidates = {}
        for w in sent_target["adjectives"]:
            candidates[w] = [(w, self.evaluator.value_evaluation(w))]
            synsets = Word(w).get_synsets(pos=ADJ)[:max_synset_len]
            properties = self.generator_utils.get_properties_adjective(w)
            for syn in synsets:
                for lemma in syn.lemmas():
                    antonyms = lemma.antonyms()
                    for a in antonyms:
                        val = self.evaluator.value_evaluation(a.name().lower())
                        candidates[w].append((self.generator_utils.right_form_adjective(a.name().lower(), properties), val))

        return candidates

    def _flatten(self, A, V):
        """
        Flattens the multidimensional array
        """
        if not A:
            return V
        for c in A:
            if not c: return V
            if type(c[0]) == str:
                V.append(" ".join(c))
            else: # it's still a list
                self._flatten(c, V)
        return V

    def fix_missing(self, set_tweets, original_sents):
        """
        Prevents creating empty candidates
        """
        res = []
        full_original_sents = [" ".join(s["tokens"]) for s in original_sents]
        for s1, s2 in zip(set_tweets, full_original_sents):
            if not s1:
                res.append([s2]) # add the original as candidate if no candidates are found
            else:
                res.append(s1)
        return res

    def generate(self):
        """
        Utilizes recursive helper function. Forms the final genotypes which are used to create combinations
        :return: candidates per sentence [[C1], [C2]...,[CN]]
        """
        max_recursion = 3
        max_synset_len = 10
        res = []
        for (i, s) in enumerate(self.pos_sentences):
            print("\t-Processing candidates for {}th sentence".format(i))
            verb_candidates = self.get_n_highest(self.negatize_verbs(s, max_synset_len), n=4)
            adj_candidates = self.get_n_highest(self.negatize_adjectives(s, max_synset_len), n=2)
            noun_candidates = self.get_n_highest(self.negatize_nouns(s, max_synset_len), n=3)
            res.append(self.replace_candidates_to_original(s, verb_candidates, adj_candidates, noun_candidates, max_recursion))

        tweets_per_sent = [self._flatten(res[i], []) for (i, s) in enumerate(self.pos_sentences)]
        set_tweets_per_sent = [list(set(sent)) for sent in tweets_per_sent]  # throw away duplicates
        print("\t-Generation done. Found {} candidates for {} sentences".format(sum([len(s) for s in set_tweets_per_sent]), len(self.pos_sentences)))
        return self.fix_missing(set_tweets_per_sent, self.pos_sentences)
