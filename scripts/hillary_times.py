import parseSQL
import ngram
import corpus
import utils

HILLARY = 80

def emailsByTimes():
  timeAndEmails  = parseSQL.getEmailsAndTimes(HILLARY)
  for key in timeAndEmails.keys():
      print "HOUR", str(key) + ":00"
      words_dict = utils.basic_count(timeAndEmails[key])
      print "number of distinct words", len(words_dict)
      print "top 5 words", sorted(words_dict, key=words_dict.get,reverse=True)[:5]
      n = ngram.NGram(2, 'word', words_dict)
      print n.display_stats()
 
def main():
  emailsByTimes() 

if __name__ == "__main__":
  emailsByTimes()
