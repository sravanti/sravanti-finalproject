import os

root_path = "output/"
def process_file(filename):
  subject_lines = []
  text = {}
  currentSenderId = ""
  with open(filename) as infile:
    for line in infile:
      line = line.split(',')
      print line
      senderPersonId = line[0]
      if senderPersonId:
        currentSenderId = senderPersonId
      if not text[currentSenderId]: 
        text[currentSenderId] = ""
      else:
        text[currentSenderId] = text[currentSenderId] + line[1]
      
    return text
    
