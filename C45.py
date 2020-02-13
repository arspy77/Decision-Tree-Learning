from collections import Counter
import DLT


class C45Node(Node):
    #tambahin depth biar bisa nge prun dari yang paling dalam
    def __init__(self, label=None, depth=0):
        super().__init__(self,label)
        self.depth = depth
        
    def add_child(self, idt, child):
        child.depth = self.depth+1
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
            
class ID3:
    def __init__(self, attr):
        self._node = None
        self._attr_dict = {}
        for idx, att in enumerate(attr):
            self._attr_dict[att] = idx

    def train(self, data, target):
        self.node = self._recur_ID3(data, target, self._attr_dict)

    def test(self, row):
        return self._recur_test(row, self._node)

    @classmethod
    def _check_label(cls, target):
        value, count = Counter(target).most_common()[0]
        return value, count == len(target)

    @classmethod
    def _plogp(cls, value):
        if value == 0:
            return 0
        return value * log2(value)

    @classmethod
    def _entropy(cls, target):
        result = 0
        count_total = len(target)
        for _, count in Counter(target).most_common():
            result -= cls._plogp(count/count_total)
        return result

    @classmethod
    def _divide_target_by_attr(cls, data, target, idx):
        attr_label = {}
        for idt, row in enumerate(data):
            value = row[idx]
            if value not in attr_label:
                attr_label[value] = []
            attr_label[value].append(target[idt])
        return attr_label
    
    @classmethod
    def best_attr(cls, data, target, attr_dict):
        E = cls._entropy(target)
        max_gain = 0
        max_attr = None
        for att in attr_dict:
            idx = attr_dict[att]
            E_sum = 0
            targets = cls._divide_target_by_attr(data, target, idx)
            for key in targets:
                targ = targets[key]
                E_sum += cls._entropy(targ) * len(targ) / len(target)
            if E - E_sum > max_gain:
                max_gain = E - E_sum
                max_attr = att
        return att
            
    @classmethod
    def _divide_data_by_attr(cls, data, idx):
        attr_data = {}
        for row in data:
            value = row[idx]
            if value not in attr_data:
                attr_data[value] = []
            attr_data[value].append(row)
        return attr_data

    @classmethod
    def _recur_ID3(cls, data, target, attr_dict):
        label, all_same_label = cls._check_label(target)
        if all_same_label or not attr_dict:
            return Node(label)
        
        att = best_attr(data, target, attr_dict)
        node = Node(att)
        idx = attr_dict[att]
        datas = cls._divide_data_by_attr(data, idx)
        targets = cls._divide_target_by_attr(data, target, idx)
        new_attr_dict = attr_dict.copy()
        del new_attr_dict[idx]
        for value in datas:
            child = cls._recur_ID3(datas[value], targets[value], new_attr_dict)
            node.add_child(value, child)
        node.add_child('__default__', Node(label))
        return node

    def _recur_test(self, row, node):
        if not node.children:
            return node.label
        else:
            idx = self._attr_dict[node.label]
            if row[idx] not in node.children:
                return self._recur_test(row, node.children['__default__'])
            else:
                return self._recur_test(row, node.children[row[idx]]) 

# class C45(ID3):
#     def __init__(self):
#         super.__init__(self)
#     def alt_select_best(self,cls, data, target, attr_dict):
#         E = cls._entropy(target)
#         max_gain = 0
#         max_attr = None
#         for att in attr_dict:
#             idx = attr_dict[att]
#             E_sum = 0
#             targets = cls._divide_target_by_attr(data, target, idx)
#             for key in targets:
#                 targ = targets[key]
#                 E_sum += cls._entropy(targ) * len(targ) / len(target)
#             if E - E_sum > max_gain:
#                 max_gain = E - E_sum
#                 max_attr = att
#         return att

    
        
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
    id3 = ID3(attr)
    id3.train(data, label)

    for row in data:
        print(id3.test(row))