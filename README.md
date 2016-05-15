#Hillary's Inbox: A text analysis of (a subset of) emails sent and received by Hillary Clinton on her private server

Final writeup: http://sravantitekumalla.com/2016/05/14/hillarys-inbox/

This is the set of scripts I used to analyze Hillary Clinton's released emails
during her time as secretary of state. I've included not only my scripts, but
my results as well, including the results of running a latent direct allocation
analysis and k-means clustering. I also took a look at vocabulary differences
between different groups of people (males vs females, ambassadors vs staffers)
and included the results of that analysis as well.

As per the final project specifications, here's a brief description of what
each script does:

* cluster.py - does the k-means analysis
* contextvectors.py - creates context vectors for a document. Added onto
functionality coded for A5 to output dictionary with word frequencies as well.
* corpus.py - analyzes a document and returns number of tokens and sentences, as well as average sentence and word length.
* dictionary.py - takes two csv files and outputs a dictionary of the
 difference between both sets (words that appear in one dictionary but not the
other)
* docterm.py - computes tf-idf for each document.
* hillary_times.py - sorts emails by time and returns statistics about average
 length of email per hour
* lda_analysis.py - performs LDA analysis on corpus
* ngram.py - calculates ngrams for document.
* parseSQL.py - queries database for emails matching criteria like emails from
 a certain senderID or getting all emails from members of a category.
* utils.py - helper funtions used throughout other files.

