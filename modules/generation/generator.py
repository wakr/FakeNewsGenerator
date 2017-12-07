from modules.evaluator import Evaluator
from modules.generation.transformer import explore_space
from textblob import Word
from textblob.wordnet import ADJ, VERB, NOUN
from modules.generation.generator_utils import GeneratorUtils

import random

class Generator:
    def __init__(self, pos_sentences):
        self.pos_sentences = pos_sentences
        self.evaluator = Evaluator()
        self.generator_utils = GeneratorUtils()

    def replace_candidates_to_original(self, target, verbs_c, adjectives_c, nouns_c, max_recursion, current=0):
        generations = []
        if current == max_recursion:
            return generations
        for v in verbs_c.keys():
            for candidate in verbs_c[v]:
                temp_tokens = list(target["tokens"])
                for (i, t) in enumerate(temp_tokens):
                    if t == v:
                        temp_tokens[i] = candidate[0]  # tuple (word, score)
                        generations.append(temp_tokens)

        for a in adjectives_c.keys():
            for candidate in adjectives_c[a]:
                temp_tokens = list(target["tokens"])
                for (i, t) in enumerate(temp_tokens):
                    if t == a:
                        temp_tokens[i] = candidate[0]  # tuple (word, score)
                        generations.append(temp_tokens)

        for n in nouns_c.keys():
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
        res = {}
        for k in candidate_scores.keys():
            cands = candidate_scores[k]
            top_n = sorted(cands, key=lambda x: x[1], reverse=True)[:n]
            res[k] = top_n
        return res

    def replacement_allowed(self, word):
        not_list = ['was', 'were', 'is', 'are', 'have', 'has', 'had']
        for not_word in not_list:
            if word == not_word:
                return False
        return True

    def negatize_verbs(self, sent_target, max_synset_len=3):
        candidates = {}
        flatten = lambda l: [item for sublist in l for item in sublist]
        for w in sent_target["verbs"]:
            candidates[w] = [(w, self.evaluator.value_evaluation(w))]
            properties = self.generator_utils.get_properties(w)
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
                val = self.evaluator.value_evaluation(l.name())
                candidates[w].append((self.generator_utils.right_form(l.name(), properties), val))
        return candidates

    def negatize_nouns(self, sent_target, max_synset_len=3):
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
                val = self.evaluator.value_evaluation(l.name())
                candidates[w].append((l.name(), val))
        return candidates

    def negatize_adjectives(self, sent_target, max_synset_len=3):
        candidates = {}
        for w in sent_target["adjectives"]:
            candidates[w] = [(w, self.evaluator.value_evaluation(w))]
            synsets = Word(w).get_synsets(pos=ADJ)[:max_synset_len]
            for syn in synsets:
                for lemma in syn.lemmas():
                    antonyms = lemma.antonyms()
                    for a in antonyms:
                        val = self.evaluator.value_evaluation(a.name())
                        candidates[w].append((a.name(), val))

        return candidates

    def _flatten(self, A, V):
        if not A:
            return V
        for c in A:
            if not c: return V
            if type(c[0]) == str:
                V.append(" ".join(c))
            else: # it's still a list
                self._flatten(c, V)
        return V

    def generate(self):
        """
        :return: candidates per sentence [[C1], [C2]...,[CN]]
        """
        max_recursion = 3
        max_synset_len = 10
        res = []
        for (i, s) in enumerate(self.pos_sentences):
            verb_candidates = self.get_n_highest(self.negatize_verbs(s, max_synset_len), n=4)
            adj_candidates = self.get_n_highest(self.negatize_adjectives(s, max_synset_len), n=2)
            noun_candidates = self.get_n_highest(self.negatize_nouns(s, max_synset_len), n=3)
            res.append(self.replace_candidates_to_original(s, verb_candidates, adj_candidates, noun_candidates, max_recursion))

        tweets_per_sent = [self._flatten(res[i], []) for (i, s) in enumerate(self.pos_sentences)]
        set_tweets_per_sent = [list(set(sent)) for sent in tweets_per_sent]  # throw away duplicates

        return set_tweets_per_sent
