import sys
import corpus
from utils import basic_count
import nltk
import codecs
from gensim import corpora, models, utils

class EmailCorpus:
  """Class for topic modeling"""
  def __init__(self, filename):
    self.tokenized_text = corpus.tokenize(filename)
    self.dictionary = corpora.Dictionary(self.tokenized_text)
    self.corpus = [self.dictionary.doc2bow(text) for text in self.tokenized_text]

  def ldaModel(self):
    lda = models.ldamodel.LdaModel(corpus=self.corpus, 
                                   id2word=self.dictionary,
                                   #eval_every=5,
                                   passes=20,
                                   num_topics=20)

    #top_words = [[word for word, _ in lda.show_topic(topicno, topn=50)] for topicno in range(lda.num_topics)]

    return lda


def doc_topics(lda, doc):
    """Takes a document and returns the models most
       closely associated with the document based on
       the given LDA model."""

    doc_tokenized = corpus.tokenize(doc)
    doc_dictionary = corpora.Dictionary(doc_tokenized)
    doc_bow = corpora.Dictionary.doc2bow(doc_dictionary)
    return lda[doc_bow]
    

if __name__ == '__main__':
    #filename = sys.argv[1]
    e = EmailCorpus('../output/senders.txt')
    lda = e.ldaModel()
    lda.save('LDAMODEL')
    #topics = doc_topics(lda, 'output/senders/female.txt')
    #print "topics", topics
