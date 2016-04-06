import corpus
import sys
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

  def tokenize(filename, casefold=True, stopwords=True):
    """Read a text file and return a list of sentences,
    where each sentences is a list of tokenized words,
    using NLTK's tokenization functions.
    """
    stoplist = set(nltk.corpus.stopwords.words('english'))
    with codecs.open(filename,'r','utf8') as f:
      text = f.read()
      result = [word_tokenize(s) for s in sent_tokenize(text)]
      if casefold:
        result = [[word.lower() for word in sentence] for sentence in result]
      if stopwords:
        result = [[word for word in sentence if word not in stoplist] for sentence in result] 
      return result
      f.close()

def ldaModel(cor):
  lda = models.ldamodel.LdaModel(corpus=e.corpus, 
                               id2word=e.dictionary,
                               alpha='auto',
                               eval_every=5,
                               num_topics=10)

  top_words = [[word for word, _ in lda.show_topic(topicno, topn=50)] for topicno in range(lda.num_topics)]

  return lda.show_topics()


if __name__ == '__main__':
    filename = sys.argv[1]
    e = EmailCorpus(filename)
    ldaModel(e)
