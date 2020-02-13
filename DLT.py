from collections import Counter
from math import log2


class Node:
    def __init__(self, label=None):
        self.label = label
        self.children = {}

    def add_child(self, idt, child):
        self.children[idt] = child

    def printTree(self, n = 0):
        for i in range(n):
            print('| ', end='')
        print('|-', end='')
        print(self.label, end='')
        if self.children:
            print(' ?') 
        else:
            print(' .')
        for child in self.children:
            for i in range(n+1):
                print('| ', end='')
            print('|-', end='')
            
            print(child, '!')
            self.children[child].printTree(n+2)


def check_label(target):
    value, count = Counter(target).most_common()[0]
    return value, count == len(target)


def plogp(value):
    if value == 0:
        return 0
    return value * log2(value)

def entropy(target):
    result = 0
    count_total = len(target)
    for _, count in Counter(target).most_common():
        result -= plogp(count/count_total)
    return result

def divide_target_by_attr(data, target, idx):
    attr_label = {}
    for idt, row in enumerate(data):
        value = row[idx]
        if value not in attr_label:
            attr_label[value] = []
        attr_label[value].append(target[idt])
    return attr_label

def best_attr(data, target, attr):
    E = entropy(target)
    max_gain = 0
    max_attr = None
    for idx in attr:
        E_sum = 0
        targets = divide_target_by_attr(data, target, idx)
        for key in targets:
            targ = targets[key]
            E_sum += entropy(targ) * len(targ) / len(target)
        if E - E_sum > max_gain:
            max_gain = E - E_sum
            max_attr = idx
    return max_attr, attr[max_attr]
        
def divide_data_by_attr(data, idx):
    attr_data = {}
    for row in data:
        value = row[idx]
        if value not in attr_data:
            attr_data[value] = []
        attr_data[value].append(row)
    return attr_data

def recur_ID3(data, target, attr):
    label, all_same_label = check_label(target)
    if all_same_label or not attr:
        return Node(label)
    
    idx, att = best_attr(data, target, attr)
    node = Node(att)
    datas = divide_data_by_attr(data, idx)
    targets = divide_target_by_attr(data, target, idx)
    new_attr = attr.copy()
    del new_attr[idx]
    for value in datas:
        child = recur_ID3(datas[value], targets[value], new_attr)
        node.add_child(value, child)
    node.add_child('default', Node(label))
    return node

def ID3(data, target, attr):
    attr_dict = {}
    for idx, att in enumerate(attr):
        attr_dict[idx] = att
    node = recur_ID3(data, target, attr_dict)
    node.printTree()
    return node

def test(row, attr, node):
    if not node.children:
        return node.label
    else:
        idx = attr.index(node.label)
        if row[idx] not in node.children:
            return test(row, attr, node.children['default'])
        else:
            return test(row, attr, node.children[row[idx]]) 

if __name__ == '__main__':
    data = [['sunny','hot','high','weak'],
            ['sunny','hot','high','strong'],
            ['overcast','hot','high','weak'],
            ['rainy','mild','high','weak'],
            ['rainy','cool','normal','weak'],
            ['rainy','cool','normal','strong'],
            ['overcast','cool','normal','strong'],
            ['sunny','mild','high','weak'],
            ['sunny','cool','normal','weak'],
            ['rainy','mild','normal','weak'],
            ['sunny','mild','normal','strong'],
            ['overcast','mild','high','strong'],
            ['overcast','hot','normal','weak'],
            ['rainy','mild','high','strong']]
    label = ['no', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'no']
    attr = ['outlook','temp','humidity','windy']
    node = ID3(data, label, attr)

    for row in data:
        print(test(row, attr, node))

    # data = [[0, 0, 0],
    #         [0, 0, 1],
    #         [0, 1, 0],
    #         [0, 1, 1],
    #         [1, 0, 0],
    #         [1, 0, 1],
    #         [1, 1, 0],
    #         [1, 1, 1]]
    # label = range(8)
    # attr = ['A', 'B', 'C']
    # node = ID3(data, label, attr)

    # for row in data:
    #     print(test(row, attr, node))


# outlook?
# -sunny !
# --humidity?
# ---high !
# ----no.
# ---normal !
# ----yes.
# -overcast !
# --yes.
# -rainy !
# --windy?
# ---weak !
# ----yes.
# ---strong !
# ----no.

# A ?
# -0 !
# --B ?
# ---0 !
# ----C ?
# -----0 !
# ------0 .
# -----1 !
# ------1 .
# -----default !
# ------0 .
# ---1 !
# ----2 .
# ---default !
# ----0 .
# -1 !
# --4 .
# -default !
# --0 .
# 0
# 1
# 2
# 2
# 4
# 4
# 4
# 4