from collections import Counter
from ID3 import Node, ID3


class C45Node(Node):
    def __init__(self, label=None, depth=0):
        super().__init__(label)
        self.pruneable = True
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
    def __init__(self, attr, node_type=C45Node):
        super().__init__(attr, node_type)

    def prune(self, data, target):
        for row, value in zip(data, target):
            self._recur_test_prune(row, value, self._node)
        self._recur_prune(self._node)

    @classmethod
    def _best_attr(cls, data, target, attr_dict):
        E = cls._entropy(target)
        max_gain = 0
        max_attr = None
        max_threshold = None
        for att in attr_dict:
            idx = attr_dict[att]
            threshold = 0
            gain = 0
            if type(data[0][idx]) == int or type(data[0][idx]) == float:
                threshold, gain = cls._calc_gain_continuous(data, target, idx)
            else:
                threshold, gain = cls._calc_gain(data, target, idx)
            if gain > max_gain:
                max_gain = gain
                max_attr = att
                max_threshold = threshold
        return max_attr, max_threshold
    
    def _missing_values(self,data):
        if data != []:
            most_common = []
            for n in range(len(data[0])):
                col = [row[n]for row in data]
                most_common_n, _ = Counter(col).most_common()[0]
                most_common.append(most_common_n)
            for i in range(len(data)):
                for j in range(len(data[0])):
                    if data[i][j] == '?':
                        data[i][j] = most_common[j]
        return data

    def train(self, data, target):
        data = self._missing_values(data)
        print(data)
        self._node = self._recur_train(data, target, self._attr_dict)

    def _recur_test_prune(self, row, value, node):
        if not node.children:
            return
        if node.children['__default__'].label != value:
            node.pruneable = False
        idx = self._attr_dict[node.label]
        if row[idx] not in node.children:
            self._recur_test_prune(row, value, node.children['__default__'])
            return
        self._recur_test_prune(row, value, node.children[row[idx]]) 

    @classmethod
    def _recur_prune(cls, node):
        if node.pruneable:
            node.label = node.children['__default__'].label
            node.children = {}
            return
        for child in node.children:
            cls._recur_prune(node.children[child])

    @classmethod
    def _calc_gain(cls, data, target, idx):
        E_sum = 0
        split_sum = 0
        targets = cls._divide_target_by_attr(data, target, idx)
        for key in targets:
            targ = targets[key]
            E_sum += cls._entropy(targ) * len(targ) / len(target)
            split_sum -= cls._plogp(len(targ) / len(target))
        if split_sum == 0:
            gain = float('inf')
        else:
            gain = (E - E_sum) / split_sum
        return gain, None

    @classmethod
    def _calc_gain_continuous(cls, data, target, idx):
        column = [row[idx] for row in data]
        value = list(set(column))

        if len(value) <= 1:
            return None

        max_gain = 0
        for val in value[0:-1]:
            small_target = [target[idt] for idt, row in enumerate(data) if row[idx] <= val]
            big_target = [target[idt] for idt, row in enumerate(data) if row[idx] > val]
            gain = cls._entropy(target) - len(small_target) / len(target) * cls._entropy(small_target) - len(big_target) / len(target) * cls._entropy(big_target)
            if gain > max_gain:
                max_gain = gain
                threshold = val
        return threshold, max_gain

    def _recur_train(self, data, target, attr_dict):
        label, all_same_label = self._check_label(target)
        if all_same_label or not attr_dict:
            return self._node_type(label)
        
        att, threshold = self._best_attr(data, target, attr_dict)
        node = self._node_type((att, threshold))
        idx = attr_dict[att]
        datas = self._divide_data_by_attr(data, idx, threshold)
        targets = self._divide_target_by_attr(data, target, idx, threshold)
        new_attr_dict = attr_dict.copy()
        del new_attr_dict[att]
        for value in datas:
            child = self._recur_train(datas[value], targets[value], new_attr_dict)
            node.add_child(value, child)
        node.add_child('__default__', self._node_type(label))
        return node

    @classmethod
    def _divide_data_by_attr(cls, data, idx, threshold):
        attr_data = {}
        for row in data:
            value = None
            if threshold is None:
                value = row[idx]
            else:
                value = row[idx] <= threshold
            if value not in attr_data:
                attr_data[value] = []
            attr_data[value].append(row)
        return attr_data

    def _divide_target_by_attr(cls, data, target, idx, threshold):
        attr_label = {}
        for idt, row in enumerate(data):
            value = None
            if threshold is None:
                value = row[idx]
            else:
                value = row[idx] <= threshold
            if value not in attr_label:
                attr_label[value] = []
            attr_label[value].append(target[idt])
        return attr_label

    def _recur_test(self, row, node):
        if not node.children:
            return node.label
        idx = self._attr_dict[node.label[0]]
        threshold = node.label[1]
        if threshold is not None:
                return self._recur_test(row, node.children[row[idx] <= threshold])
        if row[idx] not in node.children:
            return self._recur_test(row, node.children['__default__'])
        return self._recur_test(row, node.children[row[idx]])

    
    
        
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
    data = [[0, 0], [0, 1], [1, 0], [1, 1], [0, '?'], ['?', 0]]
    label = [0, 0, 1, 1, 1, 1]
    attr = [2, 3]
    c45 = C45(attr)
    c45.train(data, label)
    # c45.prune([[0, 0]], [0])
    c45._node.print_tree()

    for row in data:
        print(c45.test(row))
