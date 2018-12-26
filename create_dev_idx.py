import random, os
def create(fin, fout, n=200):
    N = len(open(fin).readlines())
    idxList = range(1, N+1)
    random.shuffle(idxList)
    lines = idxList[:n]
    lines = [str(t) for t in lines]
    open(fout, 'w').write('\n'.join(lines))

if __name__ == '__main__':
    create('../device_shrink/device_shrink.tok.raw', '../device_shrink/device_shrink.dev_idx')
