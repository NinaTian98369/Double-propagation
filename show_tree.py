from __future__ import print_function

def read_lines(fname):
    return open(fname).readlines()

def read_tree(tok_line, parent_line, rel_line, tag_line):
    flag = 0
    tokens = tok_line.lower().split()
    parents = [int(t) for t in parent_line.split()]
    relations = rel_line.split()
    tags = tag_line.split()
    if len(tokens) != len(tags):
        print(tokens)
        print(len(tokens))
        print(tags)
        print(len(tags))
    nodes = [{}]+[{} for j in range(len(tokens))]
    for j in range(len(tokens)):
        nodes[j+1]['parent'] = parents[j]
        nodes[j+1]['id'] = j+1
        nodes[j+1]['word'] = tokens[j]
        nodes[j+1]['rel'] = relations[j]
        nodes[j+1]['pos'] = tags[j]        
        nodes[parents[j]].setdefault('children', [])
        nodes[parents[j]]['children'].append(j+1)
        if parents[j] == 0:
            root = nodes[j+1]
    if len(nodes) == 1:
        root = {}
    tree = (root, nodes)
    return tree

def print_tree(tree):
    if len(tree) == 2:
        print (' '.join([n['word'] for n in tree[1][1:]]))
        print ('=='*8)
        tree = tree[0]
    print (tree['id'], tree['word'], tree['rel'], tree['pos'])
    if 'children' in tree:
        id_list = [t['id'] for t in tree['children']]
        print(id_list)
        print('--'*5)
        for child in tree['children']:
            print_tree(child)
    else:
        print ('~~'*8)

'''
if __name__=="__main__":
    #trees = read_trees('restaurant-2015.test.toks', 'restaurant-2015.test.parents', 'restaurant-2015.test.rels', '../raw/restaurant-2015.test.tag.raw')
    direc = '/home/yingding/SequenceLabeling/external/dependency/'
    trees = read_trees(direc+'laptop.toks', direc+'laptop.parents', direc+'laptop.rels', direc+'laptop.pos_tag')
    trees = [{}] + trees
'''
