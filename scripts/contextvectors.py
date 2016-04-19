"""Build context vectors of word types from a corpus,
reduce dimensionality with singular value decomposition,
store vectors."""

import scipy
from utils import *
import argparse
import time
import numpy

__author__='Sravanti and Nina'

def count_context_vectors(filename, window, freqthresh):
    """Estimate count context vectors for each word,
    with at most window number of context tokens on either side of the sentence.
    Assume filename contains one tokenized sentence per line.
    Ignore words and contexts with less than freqthresh count
    Return a list consisting of
    1. a list of the m word types with at least freqthresh count, sorted in decreasing order of frequency.
    2. an array with m rows and m+2 columns,
    where row i is the vector for the ith word in the above list,
    column i is the ith word used as context (upto m),
    column m is <s> used as context, and column m+1 is </s> used as context.
    """

    text, wordcounts = parsetextfile(filename) # read text and get word frequencies
    threshold_dict = {k: v for k, v in wordcounts.iteritems() if v >= freqthresh}
    wordtypes = sorted(threshold_dict.items(), key=lambda x: x[1])
    wordtypes = [w[0] for w in wordtypes]
    wordtypes_dict = {k: index for index, k in enumerate(wordtypes)}

    matrix = numpy.zeros((len(wordtypes), len(wordtypes) + 2))

    for sentence in text:
        for wi, word in enumerate(sentence):
            beginningtag = False
            endtag = False
            if word in threshold_dict:
                word_index = wordtypes_dict[word]
                if wi < window:
                    beginningtag = True
                    lower = 0
                    if (wi + window) > (len(sentence) - 1):
                        endtag = True
                        higher = len(sentence) - 1
                    else:
                        higher = wi + window
                elif (wi + window) > (len(sentence) - 1):
                    endtag = True
                    higher = len(sentence) -1 
                    lower = wi - window
                else:
                    lower = wi - window
                    higher = wi + window 
                context_window = sentence[lower:wi] + sentence[wi+1:higher+1]
                for w in context_window:
                    if w in threshold_dict:
                        w_index = wordtypes_dict[w]
                        matrix[w_index, word_index] += 1
                if beginningtag:
                    matrix[word_index, len(wordtypes)] += 1
                if endtag:
                    matrix[word_index, len(wordtypes) + 1] += 1

    return [wordtypes, matrix]
            

def ppmi(vectors):
    """Compute PPMI vectors from count vectors.
    """
    # Do not modify
    rowsum = scipy.sum(vectors, axis=0)  # sum each column across rows (count of context c)

    # remove all-zero columns
    nonzerocols = rowsum>0
    rowsum = rowsum[nonzerocols]
    vectors = vectors[:, nonzerocols]

    colsum = scipy.sum(vectors, axis=1)  # sum each row across columns (count of word w)
    allsum = scipy.sum(rowsum)  # sum all values in matrix

    # get p(x, y)/(p(x)*p(y))
    vectors/=colsum[:, scipy.newaxis] # count_ij/count_i*
    vectors/=rowsum # count_ij/(count_i* * count_j*)
    vectors *= allsum # prob_ij/(prob_i* * prob_j*)

    # get log, floored at 0
    vectors = scipy.log2(vectors) # will give runtime warning for log(0); ignore
    vectors[vectors<0] = 0  # get indices where value<0 and set them to 0

    return vectors

def main():
    # Do not modify
    start = time.time()

    parser = argparse.ArgumentParser(description='Build context vectors.')
    parser.add_argument('textfile', type=str, help='name of text file')
    parser.add_argument('window', type=int, help='context window')
    parser.add_argument('threshold', type=int, help='vocabulary minimum frequency')
    parser.add_argument('--ndims', type=int, default=100, help='number of SVD dimensions')
    parser.add_argument('--debug', type=bool, default=False)
    args = parser.parse_args()

    vocab, points = count_context_vectors(args.textfile+'.txt', args.window, args.threshold)
    print 'Estimated count context vectors'
    if not args.debug:  # compute PPMI and SVD before writing. if debug is True, just write the count vectors
        points = ppmi(points)
        print 'Converted to positive pointwise mutual information'
        points = dimensionality_reduce(points, args.ndims)
        print 'Reduced dimensionality'
        outfile = args.textfile+'.window'+str(args.window)+'.thresh'+str(args.threshold)
    else:
        outfile = args.textfile+'.window'+str(args.window)+'.thresh'+str(args.threshold)+'.todebug'

    with open(outfile+'.labels', 'w') as o:
        o.write('\n'.join(vocab)+'\n')
    scipy.savetxt(outfile+'.vecs', points, fmt='%.4e')
    print 'Saved to file'

    print time.time()-start, 'seconds'

if __name__=='__main__':
    main()
