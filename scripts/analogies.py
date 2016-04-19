"""Find "solutions" to a-b+c (king-man+woman = queen)
"""
from scipy.spatial.distance import cdist
import numpy
import sys

def search(wordvectors, wordlabels, wordlabelmap, a, b, c):
    aind = wordlabelmap[a]
    bind = wordlabelmap[b]
    cind = wordlabelmap[c]
    target = wordvectors[aind, :] - wordvectors[bind, :] + wordvectors[cind, :]
    cd = cdist(target[numpy.newaxis, :], wordvectors, 'cosine')
    winners = numpy.argsort(cd)[0, :4]
    # return first word that is not a, b, or c
    for i in winners:
        if i!=aind and i!=bind and i!=cind:
            return wordlabels[i]

def mainloop(filename):
    wordvectors = numpy.loadtxt(filename+'.vecs')
    wordlabels = open(filename+'.labels').read().split()
    wordlabelmap = dict([(w, i) for (i, w) in enumerate(wordlabels)])
    while True:
        a = raw_input('Enter word a: ')
        b = raw_input('Enter word b: ')
        c = raw_input('Enter word c: ')
        if a not in wordlabelmap:
            print a, 'not in vocabulary'
        elif b not in wordlabelmap:
            print b, 'not in vocabulary'
        elif c not in wordlabelmap:
            print c, 'not in vocabulary'
        else:
            winner = search(wordvectors, wordlabels, wordlabelmap, a, b, c)
            print a, '-', b, '+', c, '=', winner

if __name__=='__main__':
    mainloop(sys.argv[1])
