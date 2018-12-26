from __future__ import print_function
import show_tree as ST
import stanford_pos
import parse
import subprocess
import os
#reload(ST)


def extract_targets_R1(nodes, lexicon, labels):
    # this is for R11 and R12 in Qiu et al. 2011, inter-task

    sentiIdx = [t for t in range(1, len(nodes)) if nodes[t]['word'] in lexicon]
    #candi_pos = ['JJ', 'VB']
    #sentiIdx = [t for t in range(1, len(nodes)) if nodes[t]['pos'][:2] in candi_pos]
    targets = []

    MR = ['amod', 'advmod', 'rcmod'] #'advmod', 'rcmod', 'amod', 'pnmod' for MiniPar
    for s in sentiIdx:
        heads = []
        if nodes[s]['parent'] != 0:
            parent = nodes[s]['parent']
            if nodes[s]['rel'] in MR:
                if nodes[parent]['pos'][:2] == 'NN':
                    heads.append(parent)
                    # O-amod->T

                if 'children' in nodes[parent]:
                    for c in nodes[parent]['children']:
                        if nodes[c]['rel'][:5] == 'nsubj' and nodes[c]['pos'][:2] == 'NN':
                            heads.append(c)
                            # T-nsubj->H<-amod-O

        if 'children' in nodes[s]:
            for c in nodes[s]['children']:
                if nodes[c]['rel'][:5] == 'nsubj' and nodes[c]['pos'][:2] == 'NN':
                    heads.append(c)
                    # T-nsubj->O
                '''
                if nodes[c]['rel'][:4] == 'dobj' and nodes[c]['pos'][:2] == 'NN':
                    heads.append(c)
                    # T-dobj->O
                '''
        # this is for expanding the opinion targets from single word to phrases
        for head in heads:
            '''
            string = nodes[head]['word']
            targets.append(string)
            labels[head - 1] = 'B-ASP'
            '''
            #span = get_target_based_on_head(nodes, head, lexicon)
            #string = ' '.join([nodes[idx]['word'] for idx in range(span[0], span[1]+1)])
            string = nodes[head]['word']
            targets.append(string)

            span = get_target_based_on_head(nodes, head, lexicon)
            labels[span[0]-1] = 'B-ASP'
            if span[1] > span[0]:
                for idx in range(span[0], span[1]):
                    labels[idx] = 'I-ASP'
    return targets, labels

def extract_targets_R3(nodes, lexicon, last_targets):
    # this is for R31 and R32 in Qiu et al. 2011 intra-task

    sentiIdx = [t for t in range(1, len(nodes)) if nodes[t]['word'] in last_targets]
    targets = []
    labels = ['O']*(len(nodes)-1)
    #MR = ['amod', 'advmod', 'rcmod'] #'advmod', 'rcmod', 'amod', 'pnmod' for MiniPar
    for s in sentiIdx:
        heads = [s]
        if nodes[s]['parent'] != 0:
            parent = nodes[s]['parent']
            if nodes[s]['rel'][:4] == 'conj':
                if nodes[parent]['pos'][:2] == 'NN':
                    heads.append(parent)
                    # T-conj->Tj

            if 'children' in nodes[parent]:
                for c in nodes[parent]['children']:
                    if nodes[c]['rel'] == nodes[s]['rel'] and nodes[c]['pos'][:2] == 'NN' and c!=s:
                        heads.append(c)
                        # T-amod->H<-amod-Tc

        if 'children' in nodes[s]:
            for c in nodes[s]['children']:
                if nodes[c]['rel'][:4] == 'conj' and nodes[c]['pos'][:2] == 'NN':
                    heads.append(c)
                    # T<-conj-Tc

        # this is for expanding the opinion targets from single word to phrases
        for head in heads:
            '''
            string = nodes[head]['word']
            targets.append(string)
            labels[head - 1] = 'B-ASP'
            '''
            #span = get_target_based_on_head(nodes, head, lexicon)
            #string = ' '.join([nodes[idx]['word'] for idx in range(span[0], span[1]+1)])
            string = nodes[head]['word']
            targets.append(string)

            span = get_target_based_on_head(nodes, head, lexicon)
            labels[span[0]-1] = 'B-ASP'
            if span[1] > span[0]:
                for idx in range(span[0], span[1]):
                    labels[idx] = 'I-ASP'
    return targets, labels

def extract_opinions_R2(nodes, lexicon, last_targets, step1_opinion_labels):
    # this is for R11 and R12 in Qiu et al. 2011, inter-task

    sentiIdx = [t for t in range(1, len(nodes)) if nodes[t]['word'] in last_targets]
    opinions = lexicon
    #labels = ['O']*(len(nodes)-1)
    labels = step1_opinion_labels
    MR = ['amod', 'advmod', 'rcmod']

    for s in sentiIdx:
        heads = []
        if nodes[s]['parent'] != 0:
            parent = nodes[s]['parent']
            if nodes[s]['rel'][:5] == 'nsubj':
                if nodes[parent]['pos'][:2] == 'JJ':
                    heads.append(parent)
                    # T-nsubj->O
                if 'children' in nodes[parent]:
                    for c in nodes[parent]['children']:
                        if nodes[c]['rel'] in MR and nodes[c]['pos'][:2] == 'JJ':
                            heads.append(c)
                            # T-nsubj->H<-amod-O
            '''
            this is not useful
            if nodes[s]['rel'][:4] == 'dobj' and nodes[parent]['pos'][:2] == 'VB':
                heads.append(parent)
                # T-dobj>O
            '''
        if 'children' in nodes[s]:
            for c in nodes[s]['children']:
                if nodes[c]['rel'] in MR and nodes[c]['pos'][:2] == 'JJ':
                    heads.append(c)
                    # T<-amod-O

        # this is for expanding the opinion targets from single word to phrases
        for head in heads:
            string = nodes[head]['word']
            opinions.append(string)
            labels[head - 1] = 'B-OP'

    return opinions, labels

def extract_opinions_R4(nodes, lexicon, labels):
    # this is for R41 and R42 in Qiu et al. 2011, intra-task

    sentiIdx = [t for t in range(1, len(nodes)) if nodes[t]['word'] in lexicon]
    #candi_pos = ['JJ', 'VB']
    #sentiIdx = [t for t in range(1, len(nodes)) if nodes[t]['pos'][:2] in candi_pos]
    opinions = []

    #JJ = ['JJ', 'JJR', 'JJS']

    for s in sentiIdx:

        heads = [s] # before heads = []

        if nodes[s]['parent'] != 0:
            parent = nodes[s]['parent']
            if nodes[s]['rel'][:4] == 'conj':
                if nodes[parent]['pos'][:2] == 'JJ':
                    heads.append(parent)
                    # O-conj->Os

            if 'children' in nodes[parent]:
                for c in nodes[parent]['children']:
                    if nodes[c]['rel'] == nodes[s]['rel'] and nodes[c]['pos'][:2] == 'JJ' and c!=s: # before mistake, no c!=s
                        heads.append(c)
                        # O-amod->H<-amod-Oc

        if 'children' in nodes[s]:
            for c in nodes[s]['children']:
                if nodes[c]['rel'][:4] == 'conj' and nodes[c]['pos'][:2] == 'JJ':
                    heads.append(c)
                    # O<-conj-Oc

        # this is for expanding the opinion targets from single word to phrases
        for head in heads:
            string = nodes[head]['word']
            opinions.append(string)
            labels[head - 1] = 'B-OP'

    # Simply use lexicon to judge if it is a opinion word
    #for t in range(1, len(nodes)):
        #if nodes[t]['word'] in lexicon:
            #labels[t-1] = 'B-OP'

    return opinions, labels

def get_target_based_on_head(nodes, head, lexicon):
    span = [head]
    if 'children' in nodes[head]:
        for c in nodes[head]['children']:
            if nodes[c]['rel'] == 'amod' and nodes[c]['word'] not in lexicon:
                span.append(c)
            if nodes[c]['rel'] == 'nn':
                span.append(c)
            if nodes[c]['rel'] == 'prep':
                if 'children' in nodes[c]:
                    for g in nodes[c]['children']:
                        if nodes[g]['rel'] == 'pobj':
                            span.append(c)
                            span.append(g)

    if len(span) == 1:
        return [head, head]
    else:
        return [min(span), max(span)]

def double_propagation(fin_tok, fin_parent, fin_rel, fin_tag, lexicon):
    ##########Step 1##############
    step1_label_list = []
    step1_opinion_label_list = []
    step1_target_list = []
    step1_opinion_list = []
    n = 0



    print(len(fin_tok))
    print(len(fin_parent))
    print(len(fin_rel))
    print(len(fin_tag))
    for tok_line in fin_tok: 
        parent_line = fin_parent[n]
        rel_line = fin_rel[n]
        tag_line = fin_tag[n]
        print(n)
        
        tree = ST.read_tree(tok_line, parent_line, rel_line, tag_line)
        nodes = tree[1]
        init_labels = ['O'] * (len(nodes) - 1)
        step1_targets, step1_labels = extract_targets_R1(nodes, lexicon, init_labels)
        step1_target_list.extend(step1_targets)
        init_opinion_labels = ['O'] * (len(nodes) - 1)
        step1_opinions, step1_opinion_labels = extract_opinions_R4(nodes, lexicon, init_opinion_labels)
        step1_opinion_list.extend(step1_opinions)
        #lexicon_list = list(lexicon)
        #new_lexicon = set(lexicon_list.extend(step1_opinions))
        step1_label_list.append(step1_labels)
        step1_opinion_label_list.append(step1_opinion_labels)
        n += 1

    ##########Step 2##############
    new_lexicon = list(set(step1_opinion_list))
    new_targets = list(set(step1_target_list))
    label_list = []
    opinion_label_list = []
    opinions = []

    n = 0
    for tok_line in fin_tok:
        parent_line = fin_parent[n]
        rel_line = fin_rel[n]
        tag_line = fin_tag[n]
        #step1_targets = step1_label_list[n]
        step1_opinion_labels = step1_opinion_label_list[n]
        tree = ST.read_tree(tok_line, parent_line, rel_line, tag_line)
        nodes = tree[1]
        # lexicon_list = list(lexicon)
        # new_lexicon = set(lexicon_list.extend(step1_opinions))
        targets, labels = extract_targets_R3(nodes, new_lexicon, new_targets)
        # opinion_labels = step1_opinion_labels
        opinions, opinion_labels = extract_opinions_R2(nodes, new_lexicon, targets, step1_opinion_labels)
        label_list.append(labels)
        opinion_label_list.append(opinion_labels)
        n += 1
    return label_list, opinion_label_list, opinions

def extract_all_targetsandopinions(tok_file, parent_file, rel_file, tag_file, fout, fout_op):
    lexicon = set(open('opinion-words.txt').read().split())
    fin_tok = open(tok_file, 'r').readlines()
    fin_parent = open(parent_file, 'r').readlines()
    fin_rel = open(rel_file, 'r').readlines()
    fin_tag = open(tag_file, 'r').readlines()

    label_list, opinion_label_list, last_lexicon = double_propagation(fin_tok, fin_parent, fin_rel, fin_tag, lexicon)
    '''
    new_lexicon = []
    i = 1
    while len(last_lexicon) != len(new_lexicon) and i < 10:
        new_lexicon = last_lexicon
        label_list, opinion_label_list, last_lexicon = double_propagation(fin_tok, fin_parent, fin_rel, fin_tag,
                                                                          new_lexicon)
        i += 1
        print(i)
    '''
    fobj = open(fout, 'w')
    fobj_op = open(fout_op, 'w')
    for labels in label_list:
        fobj.write(' '.join(labels)+'\n')
    for opinion_labels in opinion_label_list:
        fobj_op.write(' '.join(opinion_labels)+'\n')
    fobj.close()
    fobj_op.close()
    return label_list, opinion_label_list

def conlleval(p, g, w, filename):
    '''
    INPUT:
    p :: predictions
    g :: groundtruth
    w :: corresponding words
    '''
    out = ''
    for sl, sp, sw in zip(g, p, w):
        out += 'BOS O O\n'
        for wl, wp, w in zip(sl, sp, sw):
            out += w + ' ' + wl + ' ' + wp + '\n'
        out += 'EOS O O\n\n'

    f = open(filename,'w')
    f.writelines(out)
    f.close()

    return get_perf(filename)

def get_perf(filename):
    # run conlleval.pl perl script to obtain precision/recall and F1 score
    _conlleval = 'conlleval.pl'

    proc = subprocess.Popen(["perl", _conlleval], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = proc.communicate('\n'.join(open(filename).readlines()))
    #print(stdout)
    for line in stdout.split('\n'):
        if 'accuracy' in line:
            out = line.split()
            break

    precision = float(out[6][:-2])
    recall    = float(out[8][:-2])
    f1score   = float(out[10])

    return {'p':precision, 'r':recall, 'f1':f1score}

def score_aspect(true_list, predict_list):
    correct = 0
    predicted = 0
    relevant = 0

    i = 0
    j = 0
    pairs = []
    while i < len(true_list):
        true_seq = true_list[i]
        predict = predict_list[i]

        for num in range(len(true_seq)):
            if true_seq[num] == 'B-ASP':
                if num < len(true_seq) - 1:
                    # if true_seq[num + 1] == '0' or true_seq[num + 1] == '1':
                    if true_seq[num + 1] != 'I-ASP':
                        # if predict[num] == '1':
                        if predict[num] == 'B-ASP' and predict[num + 1] != 'I-ASP':
                            # if predict[num] == '1' and predict[num + 1] != '1':
                            correct += 1
                            # predicted += 1
                            relevant += 1
                        else:
                            relevant += 1

                    else:
                        if predict[num] == 'B-ASP':
                            for j in range(num + 1, len(true_seq)):
                                if true_seq[j] == 'I-ASP':
                                    if predict[j] == 'I-ASP' and j < len(predict) - 1:
                                        # if predict[j] == '1' and j < len(predict) - 1:
                                        continue
                                    elif predict[j] == 'I-ASP' and j == len(predict) - 1:
                                        # elif predict[j] == '1' and j == len(predict) - 1:
                                        correct += 1
                                        relevant += 1

                                    else:
                                        relevant += 1
                                        break

                                else:
                                    if predict[j] != 'I-ASP':
                                        # if predict[j] != '1':
                                        correct += 1
                                        # predicted += 1
                                        relevant += 1
                                        break


                        else:
                            relevant += 1

                else:
                    if predict[num] == 'B-ASP':
                        correct += 1
                        # predicted += 1
                        relevant += 1
                    else:
                        relevant += 1

        for num in range(len(predict)):
            if predict[num] == 'B-ASP':
                predicted += 1

        i += 1

    precision = float(correct) / (predicted + 1e-6)
    recall = float(correct) / (relevant + 1e-6)
    f1 = 2 * precision * recall / (precision + recall + 1e-6)

    return precision, recall, f1

def score_opinion(true_list, predict_list):
    correct = 0
    predicted = 0
    relevant = 0

    i = 0
    j = 0
    pairs = []
    while i < len(true_list):
        true_seq = true_list[i]
        predict = predict_list[i]

        for num in range(len(true_seq)):
            if true_seq[num] == 'B-OP':
                if num < len(true_seq) - 1:
                    # if true_seq[num + 1] == '0' or true_seq[num + 1] == '3':
                    if true_seq[num + 1] != 'I-OP':
                        # if predict[num] == '3':
                        # if predict[num] == '1' and predict[num + 1] != '1':
                        if predict[num] == 'B-OP' and predict[num + 1] != 'I-OP':
                            correct += 1
                            # predicted += 1
                            relevant += 1
                        else:
                            relevant += 1

                    else:
                        if predict[num] == 'B-OP':
                            for j in range(num + 1, len(true_seq)):
                                if true_seq[j] == 'I-OP':
                                    # if predict[j] == '1' and j < len(predict) - 1:
                                    if predict[j] == 'I-OP' and j < len(predict) - 1:
                                        continue
                                    # elif predict[j] == '1' and j == len(predict) - 1:
                                    elif predict[j] == 'I-OP' and j == len(predict) - 1:
                                        correct += 1
                                        relevant += 1

                                    else:
                                        relevant += 1
                                        break

                                else:
                                    # if predict[j] != '1':
                                    if predict[j] != 'I-OP':
                                        correct += 1
                                        # predicted += 1
                                        relevant += 1
                                        break


                        else:
                            relevant += 1

                else:
                    if predict[num] == 'B-OP':
                        correct += 1
                        # predicted += 1
                        relevant += 1
                    else:
                        relevant += 1

        for num in range(len(predict)):
            if predict[num] == 'B-OP':
                predicted += 1

        i += 1

    precision = float(correct) / (predicted + 1e-6)
    recall = float(correct) / (relevant + 1e-6)
    f1 = 2 * precision * recall / (precision + recall + 1e-6)

    return precision, recall, f1

def get_result(direc, data, Type=''):

    pred_aspects_list = []
    aspects_list = []
    tokens_list = []

    with open(direc + data + '.toks'+Type, 'r') as fin1, open(direc + data + '.label.raw'+Type, 'r') as fin2, open(
                            direc + data + '.label.aux'+Type, 'r') as fin3:
        for line1 in fin1:
            tokens = line1.strip().split()
            tokens_list.append(tokens)
        for line2 in fin2:
            aspects = line2.strip().split()
            aspects_list.append(aspects)
        for line3 in fin3:
            pred_aspects = line3.strip().split()
            pred_aspects_list.append(pred_aspects)

    pred_file_name = dataset[:3] + '_targets_output.txt'+Type
    test_f1 = conlleval(pred_aspects_list, aspects_list, tokens_list, pred_file_name)
    #print('************************************************************************************************************')
    #print(Type+
    #'target results -- dataset:%s,precision:%f,recall:%f,f1:%f' % (dataset, test_f1['p'], test_f1['r'], test_f1['f1']))

    print('--------------------------------------------------------------------------')
    precise, recall, f1 = score_aspect(aspects_list, pred_aspects_list)
    print('self aspect precision:%f,recall:%f, f1:%f' % (precise, recall, f1))

    pred_opinions_list = []
    opinions_list = []
    tokens_list = []

    with open(direc + data + '.toks'+Type, 'r') as fin1, open(direc + data + '.opinion.raw'+Type, 'r') as fin2, open(
                            direc + data + '.opinion.aux'+Type, 'r') as fin3:
        for line1 in fin1:
            tokens = line1.strip().split()
            tokens_list.append(tokens)
        for line2 in fin2:
            opinions = line2.strip().split()
            opinions_list.append(opinions)
        for line3 in fin3:
            pred_opinions = line3.strip().split()
            pred_opinions_list.append(pred_opinions)

    pred_file_name = dataset[:3] + '_opinions_output.txt'+Type
    test_f1 = conlleval(pred_opinions_list, opinions_list, tokens_list, pred_file_name)
    #print('**************************************************************************')
    #print(Type+
    #'opinion results -- dataset:%s,precision:%f,recall:%f,f1:%f' % (dataset, test_f1['p'], test_f1['r'], test_f1['f1']))
    print('--------------------------------------------------------------------------')
    precise, recall, f1 = score_opinion(opinions_list, pred_opinions_list)
    print('self opinion precision:%f,recall:%f, f1:%f' % (precise, recall, f1))

if __name__ == '__main__':
    datasets = ['healthcare'] 

    for dataset in datasets:
        direc = '../amazon/' + dataset + '/'
        #data = dataset

        #if not os.path.exists(direc + data + '.toks'+'_train'):
        '''if dataset in ['laptop', 'restaurant']:
            pre_script_semeval.main(dataset)
        else:
            pre_script_semeval_rest.main(dataset)
        '''    
        #stanford_pos.main(dataset)
        #stanford_pos.main(dataset, Type='_test')
        
        #parse.main(dataset)
        #parse.main(dataset, Type='_test')

        print(dataset)

        type1 = '.txt'
        tok_file = '../amazon/healthcare/reviewText_healthcare.tok.tok.txt'
        parent_file = '../amazon/healthcare/reviewText_healthcare.parent.txt'
        rel_file = '../amazon/healthcare/reviewText_healthcare.rel.txt'
        tag_file = '../amazon/healthcare/reviewText_healthcare.pos_tag.txt'





        extract_all_targetsandopinions(tok_file, parent_file,
                                       rel_file, tag_file,
                                       direc + dataset + '.label.aux'+type1, direc + dataset + '.opinion.aux'+type1)

        '''
        type2 = '_test'
        extract_all_targetsandopinions(direc + data + '.toks'+type2, direc + data + '.parents'+type2,
                                       direc + data + '.rels'+type2, direc + data + '.pos_tag'+type2,
                                       direc + data + '.label.aux'+type2, direc + data + '.opinion.aux'+type2)

        
        print('-------------train---------------')
        get_result(direc, data, Type='_train')

        print('-------------test---------------')
        get_result(direc, data, Type='_test')
        '''