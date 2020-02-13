from collections import Counter
from ID3 import Node, ID3


class C45Node(Node):
    def __init__(self, label=None, depth=0):
        super().__init__(self, label)
        self.depth = 0
        self.set_depth(depth)
        
    def set_depth(self, depth=0):
        self.depth = depth
        for child in self.children:
            self.children[child].set_depth(depth + 1)

    def add_child(self, idt, child):
        child.set_depth(self.depth + 1)
        self.children[idt] = child

class C45(ID3):
    def __init__(self, attr):
        super().__init__(self,attr)

    def prune(self, data):
        self._recur_pruneable_true(self.node)


    @classmethod
    def _recur_pruneable_true(cls, node):
        node._pruneable = True
        for child in children:
            cls._recur_pruneable_true(node.children[child])

    @classmethod
    def _best_attr(cls, data, target, attr_dict):
        E = cls._entropy(target)
        max_gain = 0
        max_attr = None
        for att in attr_dict:
            idx = attr_dict[att]
            E_sum = 0
            split_sum = 0
            targets = cls._divide_target_by_attr(data, target, idx)
            for key in targets:
                targ = targets[key]
                E_sum += cls._entropy(targ) * len(targ) / len(target)
                split_sum -= -cls._plogp(targ) * len(targ) / len(target)
            gain = (E - E_sum) / split_sum
            if gain > max_gain:
                max_gain = gain
                max_attr = att
        return max_attr

    
        
'''
def load_dataset():
    data = []
    attr = []
    label = set()
    fr = open('','r')
    
    line = fr.readline()
    lineArr = line.strip().split()
    for i in range(len(lineArr)-1):
        attr.append(lineArr[i])
    
    for line in fr.readlines():
        lineArr = line.strip().split()
        record = []
        for i in range(len(lineArr)):
            record.append(lineArr[i])
        data.append(record)
        label.add(lineArr[i])
    
    fr.close()
    return data,label,attr

'''    

if __name__ == '__main__':
    # data = [['sunny','hot','high','weak'],
    #         ['sunny','hot','high','strong'],
    #         ['overcast','hot','high','weak'],
    #         ['rainy','mild','high','weak'],
    #         ['rainy','cool','normal','weak'],
    #         ['rainy','cool','normal','strong'],
    #         ['overcast','cool','normal','strong'],
    #         ['sunny','mild','high','weak'],
    #         ['sunny','cool','normal','weak'],
    #         ['rainy','mild','normal','weak'],
    #         ['sunny','mild','normal','strong'],
    #         ['overcast','mild','high','strong'],
    #         ['overcast','hot','normal','weak'],
    #         ['rainy','mild','high','strong']]
    # label = ['no', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'no']
    # attr = ['outlook','temp','humidity','windy']
    data = [[0, 0], [0, 1], [1, 0], [1, 1]]
    label = [0, 0, 1, 1]
    attr = [2, 3]
    id3 = ID3(attr)
    id3.train(data, label)
    id3._node.print_tree()

    for row in data:
        print(id3.test(row))