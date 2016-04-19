"""Return words closest to given word.
"""
from scipy.spatial.distance import cdist
import numpy
import sys

def search(wordvectors, wordlabels, wordlabelmap, word):
    """Return three closest words"""
    wind = wordlabelmap[word]
    target = wordvectors[wind, :]
    cd = cdist(target[numpy.newaxis, :], wordvectors, 'cosine')
    return [wordlabels[i] for i in numpy.argsort(cd)[0, 1:11]]

def mainloop(filename):
    wordvectors = numpy.loadtxt(filename+'.vecs')
    wordlabels = open(filename+'.labels').read().split()
    wordlabelmap = dict([(w, i) for (i, w) in enumerate(wordlabels)])
    print 'Loaded vectors for', len(wordlabels), 'words'
    while True:
        word = raw_input('Enter a word: ')
        if word not in wordlabelmap:
            print word, 'is not in the vocabulary'
        else:
            winners = search(wordvectors, wordlabels, wordlabelmap, word)
            print ', '.join(winners)

if __name__=='__main__':
    mainloop(sys.argv[1])
