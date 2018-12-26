from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('/Volumes/Research/double_propagation/script/', lang="en")

def main(dataset):
    root_folder = '../amazon/'
    pwd = root_folder + dataset + '/'
    prefix = 'reviewText_'
    input_file = pwd + prefix + dataset + '.tok.txt'   #'/Volumes/Research/double_propagation/amazon/reviewText_musical_instrument.tok.txt'
    pos_file = pwd + prefix + dataset + '.pos_tag.txt'
    with open(input_file, 'r') as fin, open(pos_file, 'w') as fout:
        for line in fin:
            sentence = line.strip()
            pos_string = nlp.pos_tag(sentence)
            postag = []
            for str_tuple in pos_string:
                postag.append(str_tuple[1])
            new_string = ' '.join(postag)
            fout.write(new_string+'\n')
    fout.close()

if __name__=='__main__':
    dataset = 'healthcare'  # 
    main(dataset)






