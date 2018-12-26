import os

def main(dataset, Type = ''):
    root_folder = '../data/'
    pwd = root_folder + dataset + '/'
    prefix = pwd + dataset
    input_file = prefix + '.toks' + Type
    tok_file = prefix + '.toks.tok' + Type
    parent_file = prefix + '.parents' + Type
    rel_file = prefix + '.rels' + Type
    #cmd = 'java -cp /Volumes/Research/double_propagation/script:/Volumes/Research/treelstm-master/lib/stanford-parser/stanford-parser.jar:/Volumes/Research/treelstm-master/lib/stanford-parser/stanford-parser-3.5.1-models.jar DependencyParse -tokpath %s -parentpath %s -relpath %s < %s' % (tok_file, parent_file, rel_file, input_file)
    cmd = 'java -cp /Volumes/Research/treelstm-master/lib:/Volumes/Research/treelstm-master/lib/stanford-parser/stanford-parser.jar:/Volumes/Research/treelstm-master/lib/stanford-parser/stanford-parser-3.5.1-models.jar DependencyParse -tokpath %s -parentpath % -relpath /%s < %s' % (tok_file, parent_file, rel_file, input_file)

    os.system(cmd)

######### Main Block ###########
if __name__ == '__main__':
    dataset = 'restaurant'  # ['laptop', 'restaurant']
    main(dataset)

