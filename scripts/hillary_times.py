import parseSQL
import ngram
import corpus
import utils
import codecs

HILLARY = 80

def emailsByTimes():
  timeAndEmails  = parseSQL.getEmailsAndTimes(HILLARY)
  timesSentence = {}
  for key in timeAndEmails.keys():
      print "HOUR", str(key) + ":00"
      words_dict = utils.basic_count(timeAndEmails[key])
      print "number of distinct words", len(words_dict)
      print "top 5 words", sorted(words_dict, key=words_dict.get,reverse=True)[:10]
      n = ngram.NGram(2, 'word', words_dict)
      c = corpus.Corpus('../output/hillary/times/'+str(key)+'Hour.txt')   
      timesSentence[key] = c.numtokens/c.numsents
      print c.display_stats()
      print n.display_stats()
  print timesSentence


def emailsToFiles():
  timeAndEmails = parseSQL.getEmailsAndTimes(HILLARY)
  for key in timeAndEmails.keys():
    filename = str(key) + "Hour.txt"
    with codecs.open(filename, 'w', 'utf-8') as f:
      f.write(" ".join(timeAndEmails[key]))
      f.close()

 
def main():
  emailsByTimes()

if __name__ == "__main__":
  main()
