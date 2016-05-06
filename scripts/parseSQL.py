import sqlite3
import codecs
import os
import time
from nltk.corpus import stopwords

SENDERPERSONID = 5

conn = sqlite3.connect('../database/database.sqlite')
c = conn.cursor()
c.execute('select * from Emails')
allEmails = c.fetchall()

def getAllSendersEmails():
  for row in allEmails:
      filename = str(row[0]) + ".txt"
      text = row[20].split()
      filteredList = [word for word in text if word not in stopwords.words('english')]
      filteredText = " ".join(filteredList)

      with codecs.open(filename, 'w', 'utf-8') as f:
          f.write(filteredText)
          f.close()

def getCategoryEmails(category):
  with codecs.open('categories/' + category + '.txt', 'r', 'utf-8') as f:
    category_text= f.readlines()
    members = [int(line) for line in category_text]
    filteredEmails  = filter(lambda x: x[SENDERPERSONID] in members, allEmails)
    result_text = []
    for row in filteredEmails:
      filename = category + 'emails.txt'
      text = row[20].split()
      filteredList = [word for word in text if word not in stopwords.words('english')]
      filteredText = " ".join(filteredList)
      result_text.append(filteredText) 
    with codecs.open(filename, 'w', 'utf-8') as outf:
      outf.write("\n".join(result_text))
      outf.close()

def getSenderEmails(senderId):
    filename = "ID" + str(senderId)  + ".txt"
    filteredEmails = filter(lambda x: x[SENDERPERSONID] is senderId, allEmails)
    result_text = []  
    for row in filteredEmails:
      text = row[20].split()
      filteredList = [word for word in text if word not in stopwords.words('english')]
      filteredText = " ".join(filteredList)
      result_text.append(filteredText)
    with codecs.open(filename, 'w', 'utf-8') as outf:
      outf.write("\n".join(result_text))
      outf.close()
      
    
def getEmailsAndTimes(senderId):
    filename = "Times" + str(senderId)  + ".txt"
    filteredEmails = filter(lambda x: x[SENDERPERSONID] is senderId, allEmails)
    result_text = {}
    timeCounts = {}
    for i in range(24):
      result_text[i] = []
      timeCounts[i] = 0
    for row in filteredEmails:
      text = row[20].split()
      if len(row[15]) > 0:
        try:
          timeTuple = time.strptime(row[15], '%A, %B %d, %Y %I:%M %p')
          #print "TIME TUPLE", timeTuple
        except:
          print "improper time format: ", row[15]
      if timeTuple:
        sw = stopwords.words('english')
        more = "<hrod17@clintonemail.com> H I UNCLASSIFIED U.S. Department of State Case No. Doc"
        sw += more.split() 
        filteredList = [word for word in text if word not in sw]
        timeCounts[timeTuple[3]] = timeCounts[timeTuple[3]] + 1 
        #print "BEFORE", len(result_text[timeTuple[3]])
        result_text[timeTuple[3]].extend(filteredList)
        #print "AFTER", len(result_text[timeTuple[3]])
    print "TIME COUNTS", timeCounts
    return result_text
      

def main():
  getEmailsAndTimes(80)

if __name__ == "__main__":
  main()
