import os
import codecs

def get_vocab_diff(dict1, dict2):
  """ Calculates differenes between two dictionaries. Takes input of two
dictionaries and returns a list of keys that appear in dictionary2 but not
dictionary 1"""
  diffKeys = set(dict2.keys()) - set(dict1.keys())
  diffDict= { k: dict2[k] for k in diffKeys }
  return [diffKeys, diffDict]
  

def fileToDict(filename):
  result_dict = {}
  with codecs.open(filename, 'r', 'utf-8') as f:
    lines = f.readlines()
    for line in lines:
      line = line.split()
      result_dict[line[0]] = line[1]
    return result_dict
      
