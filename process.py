import nltk, re, gensim
import numpy as np
from gensim.models import Word2Vec

def gen_word_vector_file(words, word_vectors, fout):
    lines = []
    for word in words:
        if word in word_vectors.vocab:
            vec = word_vectors[word]
            lines.append(word+' '+' '.join([str(e) for e in vec]))
        else:
            vec = np.random.uniform(-0.2, 0.2, 300)
            lines.append(word+' '+' '.join([str(e) for e in vec]))
    vec = np.random.uniform(-0.2, 0.2, 300)
    lines.append('[=num=]'+' '+' '.join([str(e) for e in vec]))
    vec = np.random.uniform(-0.2, 0.2, 300)
    lines.append('[=url=]'+' '+' '.join([str(e) for e in vec]))
    vec = np.random.uniform(-0.2, 0.2, 300)
    lines.append('[=unknown=]'+' '+' '.join([str(e) for e in vec]))

    f = open(fout, 'w')
    f.write('\n'.join(lines))
    f.close()

def process_token(fin, fout):
    words = set()
    wordFreq = dict()
    pattern = re.compile(r'\d')
    lines = open(fin).readlines()
    token_list = [l.lower().strip().split() for l in lines]
    for tokens in token_list:
        for i in range(len(tokens)):
            if pattern.search(tokens[i]):
                tokens[i] = '[=num=]'
            elif 'www' in tokens[i]:
                tokens[i] = '[=url=]'
            else:
                wordFreq.setdefault(tokens[i], 0)
                wordFreq[tokens[i]] += 1

    for tokens in token_list:
        for i in range(len(tokens)):
            if tokens[i] in ['[=num=]', '[=url=]']:
                continue
            elif wordFreq[tokens[i]] < 2:
                tokens[i] = '[=unknown=]'
            else:
                words.add(tokens[i])

    lines = [' '.join(tokens) for tokens in token_list]
    f = open(fout, 'w')
    f.write('\n'.join(lines))
    f.close()
    return words

if __name__=="__main__":
    words = process_token('../device/device.tok.raw', '../device/device.tok.exp')
    print 'loading word vectors'
    if 'word_vectors' not in locals().keys():
        word_vectors = Word2Vec.load_word2vec_format('/home/yingding/wordvec/GoogleNews-vectors-negative300.bin.gz', binary=True)
    gen_word_vector_file(words, word_vectors, '../device/device.wordvec')
