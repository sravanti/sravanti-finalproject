import sqlite3
import codecs
import os
from nltk.corpus import stopwords



conn = sqlite3.connect('output/database.sqlite')
c = conn.cursor()

def getAllSendersEmails():
  c.execute('select * from Emails')
  all_rows = c.fetchall()
  for row in all_rows:
      filename = str(row[0]) + ".txt"

      text = row[20].split()
      filteredList = [word for word in text if word not in stopwords.words('english')]
      filteredText = " ".join(filteredList)

      with codecs.open(filename, 'w', 'utf-8') as f:
          f.write(filteredText)
          f.close()



