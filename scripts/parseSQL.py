from __future__ import division
import sqlite3
import codecs
import os
import time
from nltk.corpus import stopwords

SENDERPERSONID = 5
EMAIL_TEXT = 20
TIMESTAMP = 15
HILLARY = 80
NUM_RECEIPIENTS = 264

conn = sqlite3.connect('../database/database.sqlite')
c = conn.cursor()

def getEmailsFromDB(command):
  c.execute(command)
  return c.fetchall()

def filterText(text):
  sw = stopwords.words('english')
  more = "<hrod17@clintonemail.com> H I UNCLASSIFIED U.S. Department of State Case No. Doc"
  sw += more.split() 
  filteredList = [word for word in text if word not in sw]
  filteredText = " ".join(filteredList)

def getAllSendersEmails():
   """ Aggregates all emails in dataset"""
  allEmails = getEmailsFromDB('select * from Emails')
  for row in allEmails:
      filename = str(row[0]) + ".txt"
      text = row[EMAIL_TEXT].split()
      filteredText = filterText(text)
      
      with codecs.open(filename, 'w', 'utf-8') as f:
          f.write(filteredText)
          f.close()

def getCategoryEmails(category):
  """ Aggregate emails for all members of a category list sent by Hillary and saves to file """
  with codecs.open('categories/' + category + '.txt', 'r', 'utf-8') as f:
    category_memebers = f.readlines()
    members = [int(line) for line in category_members]

    hillaryEmails = getEmailsFromDB('select ExtractedBodyText, PersonId as Receiver from Emails join EmailReceivers on EmailReceivers.EmailId = Emails.Id where Emails.SenderPersonId is 80;')

    filteredEmails  = filter(lambda x: x[1] in members, hillaryEmails)
    result_text = []
    for row in filteredEmails:
      filename = category + 'ReceiverEmails.txt'
      text = row[0].split()
      filteredText = filterText(text)
      result_text.append(filteredText) 
    with codecs.open(filename, 'w', 'utf-8') as outf:
      outf.write("\n".join(result_text))
      outf.close()

def getSenderEmails(senderId):
    """ Aggregate emails from a sender ID and save to file """
    filename = "ID" + str(senderId)  + ".txt"
    filteredEmails = filter(lambda x: x[SENDERPERSONID] is senderId, allEmails)
    result_text = []  
    for row in filteredEmails:
      text = row[EMAIL_TEXT].split()
      filteredText = filterText(text)
      result_text.append(filteredText)

    with codecs.open(filename, 'w', 'utf-8') as outf:
      outf.write("\n".join(result_text))
      outf.close()

    
def getEmailsAndTimes(senderId):
    """ Sort emails by time for a particular sender ID. Returns a dictionary of hour mapping to email text sent in that hour. """
    filename = "Times" + str(senderId)  + ".txt"
    filteredEmails = filter(lambda x: x[SENDERPERSONID] is senderId, allEmails)
    result_text = {}
    timeCounts = {}
    averageEmailLength = {}

    for i in range(24):
      result_text[i] = []
      timeCounts[i] = 0
      averageEmailLength[i] = 0

    for row in filteredEmails:
      text = row[EMAIL_TEXT].split()
      timestamp_field = len(row[TIMESTAMP]) > 0:

      if timestamp_field:
        try:
          timestamp = time.strptime(row[TIMESTAMP], '%A, %B %d, %Y %I:%M %p')
        except:
          print "improper time format: ", row[TIMESTAMP]
      if timestamp:
        HOUR = timestamp[3]
        filteredList = filterText(text)

        timeCounts[HOUR] = timeCounts[HOUR] + 1 
        result_text[HOUR].extend(filteredList)
        averageEmailLength[HOUR] += len(filteredList)

    for key in averageEmailLength.keys():
        averageEmailLength[key] = averageEmailLength[key] / timeCounts[key]
    print "AVERAGE EMAIL LENGTH", averageEmailLength

    return result_text
      
def main():
  pass
  
if __name__ == "__main__":
  main()
