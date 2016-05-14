"""Build term-document matrix from collection of documents."""

import scipy
import numpy
from utils import *
import argparse
import time
from math import log

__author__='Nina and Sravanti'

def tfidf_docterm(filename, freqthresh):
    """Estimate document-term TF-IDF vectors for each document (line in filename),
    where each column is a word, in decreasing order of frequency.
    Ignore words that appear fewer than freqthresh times.
    Return a list consisting of
    1. a list of the m word types with at least freqthresh count, sorted in decreasing order of frequency.
    2. an array with d rows and m columns,
    where row i is the vector for the ith document in filename,
    and col j represents the jth word in the above list.
    """
    text, wordcounts = parsetextfile(filename)
    threshold_dict = {k: v for k, v in wordcounts.iteritems() if v >= freqthresh}
    wordtypes = sorted(threshold_dict.items(), key=lambda x: x[1])
    wordtypes = [w[0] for w in wordtypes]
    wordtypes_dict = {k: index for index, k in enumerate(wordtypes)}
    
    matrix = numpy.zeros((len(text), len(wordtypes)))
    tf = numpy.zeros((len(text), len(wordtypes)))
    idf = numpy.zeros(len(wordtypes))

    for di, document in enumerate(text):
        for word in document:
            if word in wordtypes_dict:
                word_index = wordtypes_dict[word]
                matrix[di, word_index] += 1

    #TF step
    for di, document in enumerate(matrix):
        docterms = sum(document)
        for ti in range(len(document)):
            tf[di][ti] = matrix[di][ti] / docterms

    #IDF step
    numdocs = len(text)
    for ci in range(len(matrix[0])):
        column = matrix[:, ci] 
        numt = len(filter(lambda x: x != 0, column))
        idf[ci] = log(numdocs / numt)
    
    #result matrix
    for di in range(len(matrix)):
        for ti in range(len(matrix[0])):
            matrix[di][ti] = tf[di][ti] * idf[ti]
                        
    return [wordtypes_dict.keys(), matrix]
            
def main():
    # Do not modify
    start = time.time()

    parser = argparse.ArgumentParser(description='Build document-term vectors.')
    parser.add_argument('textfile', type=str, help='name of text file with documents on each line')
    parser.add_argument('threshold', type=int, help='term minimum frequency')
    parser.add_argument('--ndims', type=int, default=100, help='number of SVD dimensions')
    parser.add_argument('--debug', type=bool, default=False, help='debug mode?')
    args = parser.parse_args()

    terms, points = tfidf_docterm(args.textfile+'.txt', args.threshold)
    print 'Estimated document-term TF-IDF vectors'
    if not args.debug:  # compute PPMI and SVD before writing. if debug is True, just write the count vectors
        points = dimensionality_reduce(points, args.ndims)
        print 'Reduced dimensionality'
        outfile = args.textfile+'.tfidf'+'.thresh'+str(args.threshold)
    else:
        outfile = args.textfile+'.tfidf'+'.thresh'+str(args.threshold)+'.todebug'

    with open(outfile+'.dims', 'w') as o:
        o.write('\n'.join(terms)+'\n')
    scipy.savetxt(outfile+'.vecs', points, fmt='%.4e')
    print 'Saved to file'

    print time.time()-start, 'seconds'

if __name__=='__main__':
    main()
