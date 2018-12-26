import show_tree as ST
import pre_script_semeval
import stanford_pos
import parse
import subprocess
import os
reload(ST)

def conll_format(a, g, w, parents_list, deprels_list, postags_list, filename):
    '''
    INPUT:
    a :: aspect
    g :: opinion
    w :: corresponding words
    '''
    out = ''
    for aspect, opinion, sw, pa, de, pt in zip(a, g, w, parents_list, deprels_list, postags_list):
        for asp, opi, w, parent, deprel, postag in zip(aspect, opinion, sw, pa, de, pt):
            out += w + ' ' + asp + ' ' + opi + ' ' + parent + ' ' + deprel +' ' + postag + '\n'
        out += '\n'
    f = open(filename,'w')
    f.writelines(out)
    f.close()

def train_test_save(direc, data, Type=''):
    tokens_list = []
    aspects_list = []
    opinions_list = []
    parents_list = []
    deprels_list = []
    postags_list = []

    with open(direc + data + '.toks'+Type, 'r') as fin1, open(direc + data + '.label.raw'+Type, 'r') as fin2,\
        open(direc + data + '.opinion.raw' + Type, 'r') as fin3, open(direc + data + '.parents' + Type, 'r') as fin4,\
        open(direc + data + '.rels' + Type, 'r') as fin5, open(direc + data + '.pos_tag' + Type, 'r') as fin6:
        for line1 in fin1:
            tokens = line1.strip().split()
            tokens_list.append(tokens)
        for line2 in fin2:
            aspects = line2.strip().split()
            aspects_list.append(aspects)
        for line3 in fin3:
            opinions = line3.strip().split()
            opinions_list.append(opinions)
        for line4 in fin4:
            parents = line4.strip().split()
            parents_list.append(parents)
        for line5 in fin5:
            deprels = line5.strip().split()
            deprels_list.append(deprels)
        for line6 in fin6:
            postags = line6.strip().split()
            postags_list.append(postags)

    save_data_dir = direc
    if not os.path.exists(save_data_dir):
        os.mkdir(save_data_dir)
    pred_file_name = save_data_dir+ data + '.conll'+Type
    conll_format(aspects_list, opinions_list, tokens_list, parents_list, deprels_list, postags_list, pred_file_name)

if __name__ == '__main__':
    datasets = ['rest', 'laptop', 'restaurant'] #'laptop', 'restaurant'

    for dataset in datasets:
        direc = '../data/' + dataset + '/'
        data = dataset

        if not os.path.exists(direc + data + '.toks'+'_train'):
            pre_script_semeval.main(dataset)
            stanford_pos.main(dataset, Type='_train')
            stanford_pos.main(dataset, Type='_test')
            parse.main(dataset, Type='_train')
            parse.main(dataset, Type='_test')
        train_test_save(direc, data, Type='_train')
        train_test_save(direc, data, Type='_test')


