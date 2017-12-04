from modules.evaluator import Evaluator
from modules.generation.transformer import explore_space
from textblob import Word
from textblob.wordnet import ADJ, VERB, NOUN

import random

class Generator:
    def __init__(self, tokens, phrase_targets, nouns, verbs, adverbs, adjectives):
        self.tokens = tokens
        self.phrase_targets = phrase_targets
        self.nouns = nouns
        self.verbs = verbs
        self.adverbs = adverbs
        self.adjectives = adjectives
        self.evaluator = Evaluator()

    def replace_candidates_to_original(self, candidates):
        """
        Mutates the original tokens
        :param candidates: POS-candidates
        """
        for c in candidates.keys():
            for (i, t) in enumerate(self.tokens):
                if c == t:
                    self.tokens[i] = random.choice(candidates[c])[0]  # (word, score) pairs

    def get_n_highest(self, candidate_scores, n=1):
        res = {}
        for k in candidate_scores.keys():
            cands = candidate_scores[k]
            top_n = sorted(cands, key=lambda x: x[1], reverse=True)[:n]
            res[k] = top_n
        return res



    def negatize_verbs(self):
        candidates = {}
        flatten = lambda l: [item for sublist in l for item in sublist]
        for w in self.verbs:
            candidates[w] = [(w, self.evaluator.value_evaluation(w))]
            synsets = Word(w).get_synsets(pos=VERB)
            upper_meanings = []
            for ss in synsets:
                hype = flatten([h.lemmas() for h in ss.hypernyms()])
                hypo = flatten([h.lemmas() for h in ss.hyponyms()])
                upper_meanings += hype
                upper_meanings += hypo
            for l in upper_meanings:
                val = self.evaluator.value_evaluation(l.name())
                candidates[w].append((l.name(), val))
        return candidates

    def negatize_subs(self):
        candidates = {}
        flatten = lambda l: [item for sublist in l for item in sublist]
        for w in self.nouns:
            candidates[w] = [(w, self.evaluator.value_evaluation(w))]
            synsets = Word(w).get_synsets(pos=NOUN)
            upper_meanings = []
            for ss in synsets:
                hype = flatten([h.lemmas() for h in ss.hypernyms()])
                hypo = flatten([h.lemmas() for h in ss.hyponyms()])
                upper_meanings += hype
                upper_meanings += hypo
            for l in upper_meanings:
                val = self.evaluator.value_evaluation(l.name())
                candidates[w].append((l.name(), val))
        return candidates

    def negatize_adjectives(self):
        candidates = {}
        for w in self.adjectives:
            candidates[w] = [(w, self.evaluator.value_evaluation(w))]
            synsets = Word(w).get_synsets(pos=ADJ)
            print(synsets)
            for syn in synsets:
                antonyms = syn.lemmas()[0].antonyms()
                for a in antonyms:
                    val = self.evaluator.value_evaluation(a.name())
                    candidates[w].append((a.name(), val))

        return candidates

    def generate(self):
        verb_candidates = self.negatize_verbs()
        verb_candidates = self.get_n_highest(verb_candidates)
        self.replace_candidates_to_original(verb_candidates)
        adj_candidates = self.negatize_adjectives()
        adj_candidates = self.get_n_highest(adj_candidates)
        self.replace_candidates_to_original(adj_candidates)
        return self.tokens
