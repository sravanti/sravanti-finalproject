"""Cluster vectors with k-means"""

import scipy
import argparse
from scipy.spatial.distance import cdist
import codecs
import time
import operator

__author__='Nina and Sravanti'

def kmeans(points, labels, k, maxiter):
    """Cluster points (named with corresponding labels) into k groups.
    Return a dictionary mapping each cluster ID (from 0 through k-1)
    to a list of the labels of the points that belong to that cluster.
    """
    #print "points", points
    #print "labels", labels
    clusters = {}
    centroids = []

    labels_dict = {lab: i for i, lab in enumerate(labels)}
    #print "labels_dict", labels_dict
  
    #initialize centroids
    for i in range(k):
        clusters[i] = []
        centroids.append(points[i])
  
    final_cluster = {}
    while maxiter >= 0:

        #calculate distance from centroids
        distance = cdist(points, centroids)

        # assign points to clusters
        for ri, row in enumerate(distance):
            min_index, min_value = min(enumerate(row), key=operator.itemgetter(1))
            clusters[min_index].append(ri)
    
        # exit while loop if clusters have changed
        if clusters == final_cluster:
            break

        # recalculate centroids
        for ci, cluster in clusters.iteritems():
            if len(cluster) > 0:
                pts = [points[ri] for ri in cluster]
                centroids[ci] = scipy.mean(pts, axis=0) 
            else:
                centroids[ci] = points[ci]
        
        final_cluster = clusters.copy()
        for ci in clusters.keys():
            clusters[ci] = []

        maxiter -= 1 
    
    result = {}

    for ci, cluster in final_cluster.iteritems():
        for pi in cluster:
            if ci in result:
                result[ci] = result[ci] + [labels[pi]]
            else:
                result[ci] = [labels[pi]]

    return result
        
  
def main():
    # Do not modify
    start = time.time()

    parser = argparse.ArgumentParser(description='Cluster vectors with k-means.')
    parser.add_argument('vecfile', type=str, help='name of vector file (exclude extension)')
    parser.add_argument('k', type=int, help='number of clusters')
    parser.add_argument('--maxiter', type=int, default=100, help='maximum number of k-means iterations')
    args = parser.parse_args()

    #TODO: use os.path instead...
    points = scipy.loadtxt('cluster_input/' + args.vecfile + '.vecs')
    labels = codecs.open('cluster_input/' + args.vecfile + '.labels', 'r', 'utf8').read().split()

    clusters = kmeans(points, labels, args.k, args.maxiter)
    outfile = '../output/clusters/' + args.vecfile+'.cluster'+str(args.k)
    with codecs.open(outfile, 'w', 'utf8') as o:
        for c in clusters:
            o.write('CLUSTER '+str(c)+'\n')
            o.write(' '.join(clusters[c])+'\n')

    print time.time()-start, 'seconds'

if __name__=='__main__':
    main()
