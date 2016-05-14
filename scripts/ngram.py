from __future__ import division  # floating point division
from math import log
from utils import normalize, entropy

__author__='Sravanti Tekumalla'

class NGram:
    """Class for estimating n-gram probabilities from a corpus.
    Only supports simple unsmoothed unigrams this time;
    will expand to n>1 and smoothing in A2."""

    def __init__(self, n, unit, countdict):
        """store dictionary of counts, order and unit of n-gram model"""
        self.countdict = countdict
        self.n = n   # order of n-gram model
        self.unit = unit
        self.countdict = countdict

        if self.n>=1:
            self.relcounts = {1: normalize(self.countdict)}   # unigram probabilities

    def unigram_entropy(self):
        """return entropy of this unigram distribution in bits"""
        return entropy(self.relcounts[1])

    def display_stats(self):
        """summary statistics for this n-gram model"""

        print 'Estimated a {0}-gram model over {1}s'.format(self.n, self.unit)

        #print "top 5 words"
        #print sorted(self.relcounts[1].items(), key =lambda x:x[1], reverse=True)[:10]
        fword, fcount = max(self.relcounts[1].items(), key=lambda x:x[1])
        print "'{0}' is the most common {1}, occurring {2:.2%} of the time".format(fword, self.unit, fcount)

        print 'The unigram entropy is {0:.2f} bits'.format(self.unigram_entropy())

    def get_prob(self, x):
        """return unigram probability of x:
        relative frequency of x if it is known,
        0 if not
        """
        return self.relcounts[1].get(x, 0)

    def cross_entropy(self, text):
        """return the cross entropy in bits of this unigram model on
        text, which is a sequence of units (words or characters)"""
        surprisal = 0
        length = 0
        if self.unit is "character":
          text = list(text)
        elif self.unit is "word":
          text = text.split(" ")

        for char in text:
          if self.get_prob(char) != 0:
            surprisal += log(self.get_prob(char), 2)
            length = length + 1
        return -1*surprisal / length
