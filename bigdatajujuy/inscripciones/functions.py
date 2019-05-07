import re

def delete_tags(texto):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', texto)
  return cleantext