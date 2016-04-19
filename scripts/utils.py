from __future__ import division  # floating point division
from math import log
from collections import Counter, defaultdict
import scipy
import scipy.sparse.linalg

__author__='Sravanti Tekumalla'

def normalize(countdict):
    """given a dictionary mapping items to counts,
    return a dictionary mapping items to their normalized (relative) counts.
    Example: normalize({'a': 2, 'b': 1, 'c': 1}) -> {'a': 0.5, 'b': 0.25, 'c': 0.25}
    """
    total = sum(countdict.values())
    return {item: val/total for item, val in countdict.items()}

def basic_count(itemlist):
    """return a dictionary of item counts in the given sequence of items
    Example: basic_count('abac') -> {'a': 2, 'b': 1, 'c': 1}
    basic_count(['the', 'hat', 'in', 'the', 'hat']) -> {'the': 2, 'hat': 2, 'in': 1}
    """
    return dict(Counter(itemlist))

def length_count(itemlist):
    """return a dictionary mapping each length value to
    the count of items of that length
    Example: length_count(['the', 'last', 'year']) -> {3: 1, 4: 2}
    """
    return dict(Counter(len(item) for item in itemlist))

def expectation(dist):
    """from a dictionary mapping numerical items to relative counts,
    compute and return the weighted average value
    (i.e., if dist represents a random variable, return the expectation)
    Example: expectation({1: 0.5, 2: 0.25, 3: 0.25}) -> 1.75
    """
    return sum(key*val for key, val in dist.items())

def entropy(probdist):
    """given a dictionary mapping items to probabilities,
    return the entropy of the probability distribution in bits
    Example: entropy({'a': 0.5, 'c': 0.5}) -> 1.0
    entropy({'a': 0.5, 'c': 0.25, 'b': 0.25}) -> 1.5
    entropy({'a': 0.5, 'c': 0.25, 'b': 0.25, 'd': 0.0}) -> 1.5
    """
    return -sum(0 if val == 0.0 else val*log(val, 2) for val in probdist.values())

def tuple_count(itemlist, tuplen):
    """return a dictionary of tuple counts,
    where each tuple is a subsequence of length tuplen,
    from a sequence of items
    Example: tuple_count('mississippi', 3) -> {('i', 's', 's'): 2, ('m', 'i', 's'): 1, ('s', 'i', 's'): 1,
    ('s', 's', 'i'): 2, ('i', 'p', 'p'): 1, ('p', 'p', 'i'): 1, ('s', 'i', 'p'): 1}
    tuple_count(['the', 'hat', 'in', 'the', 'hat'], 2) -> {('hat', 'in'): 1, ('the', 'hat'): 2, ('in', 'the'): 1}
    """
    tups = []
    for x in range(0, (len(itemlist) - tuplen + 1)):
     tups.append(tuple(itemlist[x:x+tuplen]))
    return dict(Counter(tup for tup in tups))


#### FOLLOWING BY SRAVANA REDDY
def progressbar(ctr, eachdot, eachline):
    """Utility to show progress within loops.
    Works best with unbuffered output (python -u)
    """
    if ctr%eachdot==0:
        print '.',
    if ctr%eachline==0:
        print ctr

def parsetextfile(filename):
    """Read text in file as a list of lists of words,
    count word frequencies,
    return text and word counts.
    """
    text = []
    wordcounts = defaultdict(int)
    ctr = 0   # track lines for progressbar
    for line in open(filename):
        line = line.split()
        text.append(line)
        for word in line:
            wordcounts[word]+=1
        ctr+=1
        progressbar(ctr, 5000, 100000)
    print 'Read text and counted words'
    print ctr, 'lines and', len(wordcounts), 'word types'
    return text, wordcounts

def dimensionality_reduce(vectors, ndims):
    """Apply SVD on original sparse matrix, return reduced vectors."""
    # Do not modify
    U, s, Vh = scipy.sparse.linalg.svds(vectors, k=ndims)
    sigmatrix = scipy.matrix(scipy.diag(s))
    return U * sigmatrix

