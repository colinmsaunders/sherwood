# sherwood.py -- sherwood forest, a CLI tree utility


import sys, json


NULL_PARENT_STR = '-'
PREORDER = 1
POSTORDER = 2


def roots(forest):
    a = []
    for i in forest.values():
        if None == i[1]:
            a.append(i)
    return a


def leafs(forest):
    a = []
    for i in forest.values():
        if 0 == len(i[3]):
            a.append(i)
    return a


def parents(forest):
    a = []
    for i in forest.values():
        if 0 != len(i[3]):
            a.append(i)
    return a


def read_forest(f):
    x = {}
    for i in f:
        t = i[:-1].split('\t')
        parent = t[1]
        if NULL_PARENT_STR == parent:
            parent = None
        _id = t[0]
        rest = t[2:]
        if _id in x:
            if None != x[_id][0]:
                pass # aise Exception('duplicate key \'%s\'' % _id)
            x[_id][0] = _id
            x[_id][1] = parent
            x[_id][2] = rest
        else:
            x[_id] = [_id, parent, rest, []]
        if None != parent:
            if not parent in x:
                x[parent] = [None, None, None, []]
            x[parent][3].append(_id)
    return x


def dump_node(node):
    parent = node[1]
    if None == parent:
        parent = NULL_PARENT_STR
    s = '%s\t%s\t%s' % (node[0], parent, '\t'.join(node[2]))
    return s


def walk(forest, node_id, foo):
    node = x[node_id]
    foo(node, PREORDER)
    for child_id in node[3]:
        walk(forest, child_id, foo)
    foo(node, POSTORDER)


def stats(forest, node_id):
    stats = {}

    def walk_stats(forest, stats, node_id):
        stat = {}
        stat['node_id'] = node_id
        node = forest[node_id]
        for child_id in node[3]:
            walk_stats(forest, stats, child_id)
        stat['is_parent'] = 0 != len(node[3])
        stat['is_leaf'] = 0 == len(node[3])
        stat['children'] = len(node[3])
        if 0 == len(node[3]):
            stat['n'] = 1
            stat['leafs'] = 1
            stat['parents'] = 0
            stat['height'] = 1
            stat['width'] = 1
        else:
            stat['n'] = 1 + sum(map(lambda x: stats[x]['n'], node[3]))
            stat['height'] = 1 + max(map(lambda x: stats[x]['height'], node[3]))
            stat['width'] = max(map(lambda x: stats[x]['width'], node[3])) # FIXME: this is wrong
            stat['leafs'] = sum(map(lambda x: stats[x]['leafs'], node[3]))
            stat['parents'] = 1 + sum(map(lambda x: stats[x]['parents'], node[3]))

        if 0 != len(node[3]):
            stat['nodes_per_parent'] = stat.get('n') / float(stat.get('parents'))
            stat['leafs_per_parent'] = stat.get('leafs', 0) / float(stat.get('parents'))
            stat['node_height_density'] = stat.get('n') / float(stat.get('height'))

        stats[node_id] = stat

    walk_stats(forest, stats, node_id)
    return stats[node_id]


def main(argv):
    c = argv[0]
    if 0:
        pass
    elif 'roots' == c:
        x = read_forest(sys.stdin)
        for i in roots(x):
            sys.stdout.write(dump_node(i) + '\n')
    elif 'leafs' == c:
        x = read_forest(sys.stdin)
        for i in leafs(x):
            sys.stdout.write(dump_node(i) + '\n')
    elif 'parents' == c:
        x = read_forest(sys.stdin)
        for i in parents(x):
            sys.stdout.write(dump_node(i) + '\n')
    elif 'read' == c:
        x = read_forest(sys.stdin)
        sys.stdout.write(json.dumps(x, indent=2))
    elif 'branch' == c:
        x = read_forest(sys.stdin)
        walk(x, argv[1], lambda x, _: sys.stdout.write(dump_node(x) + '\n'))
    elif 'stats' == c:
        forest = read_forest(sys.stdin)
        x = stats(forest, argv[1])
        for i, j in x.items():
            sys.stdout.write('%s\t%s\n' % (i, j))
    else:
        raise Exception('i don\'t know how to \'%s\'' % c)


if __name__ == '__main__':
    x = main(sys.argv[1:])
    sys.exit(x)
