import re
import sys

from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('./', lang="en")

dataset = 'electronics'

if __name__ == '__main__':
  f = open('../amazon/'+ dataset +'/reviewText_' + dataset + '.txt','r')
  lines = f.readlines()
  g = open('../amazon/'+ dataset +'/reviewText_' + dataset + '.tok.txt','w')
  for line in lines :
    token_sent = nlp.word_tokenize(line)
    tokens = [nlp._convert(token).lower() for token in token_sent]
    l = ''
    l += ' '.join(tokens)
    l += '\n'
    g.write(l)

  f.close()
  g.close()