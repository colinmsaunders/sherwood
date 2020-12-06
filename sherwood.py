# sherwood.py -- sherwood forest, a CLI tree utility


import sys, json


NULL_PARENT_STR = '-'
PREORDER = 1
POSTORDER = 2


def roots(x):
    a = []
    for i in x.values():
        if None == i[1]:
            a.append(i)
    return a


def leafs(x):
    a = []
    for i in x.values():
        if 0 == len(i[3]):
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


def dump_node(x):
    parent = x[1]
    if None == parent:
        parent = NULL_PARENT_STR
    s = '%s\t%s\t%s' % (x[0], parent, '\t'.join(x[2]))
    return s


def walk(x, node, foo):
    i = x[node]
    foo(i, PREORDER)
    for j in i[3]:
        walk(x, j, foo)
    foo(i, POSTORDER)


def stats(forest, node):
    x = {}
    def observe(node, order):
        if PREORDER == order:
            if not 'depth' in x:
                x['depth'] = 0
            x['depth'] += 1
            x['max_depth'] = max(x.get('max_depth', 0), x['depth'])
            if not 'n' in x:
                x['n'] = 0
            x['n'] += 1
            if None == node[1]:
                if not 'roots' in x:
                    x['roots'] = 0
                x['roots'] += 1
            if 0 == len(node[3]):
                if not 'leafs' in x:
                    x['leafs'] = 0
                x['leafs'] += 1
        if POSTORDER == order:
            x['depth'] -= 1
    walk(forest, node, observe)
    if 0 != x.get('n'):
        x['height'] = x.get('max_depth')
    x['parents'] = x.get('n', 0) - x.get('leafs', 0)
    if 0 != x.get('parents', 0):
        x['nodes_per_parent'] = x.get('n') / float(x.get('parents'))
        x['leafs_per_parent'] = x.get('leafs', 0) / float(x.get('parents'))

    if 0 != x.get('n', 0):
        x['node_height_density'] = x.get('n') / float(x.get('max_depth'))
    return x


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
            sys.stdout.write('%s\t%g\n' % (i, j))
    else:
        raise Exception('i don\'t know how to \'%s\'' % c)


if __name__ == '__main__':
    x = main(sys.argv[1:])
    sys.exit(x)
