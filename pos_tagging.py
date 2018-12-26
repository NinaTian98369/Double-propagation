import nltk
def do_tagging(tok_file, tag_file):
    fin = open(tok_file)
    fout = open(tag_file, 'w')
    n = 0
    for line in fin:
        toks = line.strip().decode('utf-8').split()
        tags = nltk.pos_tag(toks)
        string = ' '.join([t[1] for t in tags])+'\n'
        fout.write(string)
        n += 1
        if n%int(500) == 0:
            print n
    fin.close()
    fout.close()

if __name__ == '__main__':
    import sys
    do_tagging('../data/device/device.tok.raw', '../data/device/device.pos_tag')
