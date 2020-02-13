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

class C45(ID3):
    def __init__(self,attr):
        super().__init__(self,attr)
    def alt_select_best(self,cls, data, target, attr_dict):
        E = cls._entropy(target)
        max_gain = 0
        gain_list = []
        tested_attribute = []
        max_attr = None
        for att in attr_dict:
            idx = attr_dict[att]
            E_sum = 0
            targets = cls._divide_target_by_attr(data, target, idx)
            for key in targets:
                targ = targets[key]
                E_sum += cls._entropy(targ) * len(targ) / len(target)
            gain_list.append(E-E_sum,att)
        avg_gain = sum(gain_list[0])/len(gain_list)
        for gain,att in gain_list:
            if gain > avg_gain:
                tested_attribute.append(gain,att)
        for gain,att in avg_gain
        return att

    
        
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