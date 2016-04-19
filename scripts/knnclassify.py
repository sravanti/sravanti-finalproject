from __future__ import division

"""Classify data with KNN"""

import scipy
import argparse
from scipy.spatial.distance import cdist
from scipy.stats import mode
from numpy import argsort
import codecs
import time

__author__='Sravanti and Nina'

def knn(trainpoints, traincats, testpoints, k):
    """Given training data points
    and a 1-d array of the corresponding categories of the points,
    predict category for each test point,
    using k nearest neighbors (with cosine distance).
    Return a 1-d array of predicted categories.
    """
    predicted_cats = []
    dist_matrix = cdist(testpoints, trainpoints, 'cosine')
    for pi, point in enumerate(testpoints):
        distances = dist_matrix[pi]
        min_indices = distances.argsort()[:k]
        categories = [traincats[i] for i in min_indices]
        predicted_cats.append(mode(categories)[0][0])

    return predicted_cats

def main():
    # Do not modify
    start = time.time()

    parser = argparse.ArgumentParser(description='Classify unknown point with kNN.')
    parser.add_argument('filename', type=str, help='root name of file with data (vectors, categories, train-test split)')
    parser.add_argument('k', type=int, help='k in kNN')

    args = parser.parse_args()

    points = scipy.loadtxt('cluster_input/' + args.filename+'.vecs')
    cats = scipy.loadtxt('cluster_input/' + args.filename+'.cats', dtype=int)
    traintestsplit = scipy.loadtxt('cluster_input/' + args.filename+'.ttsplit')

    # use ttsplit indices to separate out train and test data
    trainpoints = points[traintestsplit==0]
    traincats = cats[traintestsplit==0]
    testpoints = points[traintestsplit==1]
    testcats = cats[traintestsplit==1]

    # run knn classifier
    predictions = knn(trainpoints, traincats, testpoints, args.k)

    # write actual category, predict category, and text of test points, and compute accuracy
    o = codecs.open(args.filename+'.predictions', 'w', 'utf8')
    o.write('ACTUAL,PREDICTED,CORRECT?,TEXT\n')
    textfile = codecs.open(args.filename+'.txt', 'r', 'utf8')
    testindex = 0
    numcorrect = 0.
    for i in traintestsplit:
        line = textfile.readline()
        if i==1:
            o.write(str(testcats[testindex]))
            o.write(',')
            o.write(str(predictions[testindex]))
            o.write(',')
            if testcats[testindex] == predictions[testindex]:
                numcorrect += 1
                o.write('CORRECT,')
            else:
                o.write('WRONG,')
            o.write(line)
            testindex+=1
    print 'Stored predictions in', args.filename+'.predictions', 'for test points'
    acc = numcorrect*100/testindex
    print 'Accuracy: {0:.2f}%'.format(acc)

    print time.time()-start, 'seconds'

if __name__=='__main__':
    main()
