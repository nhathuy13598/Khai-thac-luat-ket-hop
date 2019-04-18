# T = {
#     "100": ['I', 'B', 'F', 'D', 'E', 'C', 'H', 'J'],
#     "200": ['F', 'G', 'A', 'D', 'C'],
#     "300": ['B', 'J', 'D', 'A', 'H'],
#     "400": ['A', 'B', 'E', 'G']
# }
# item = ('A','B','C','D','E','F','G','H','I','J')
T ={
    't100': ['i1','i2','i5'],
    't200': ['i2','i4'],
    't300': ['i2', 'i3'],
    't400': ['i1', 'i2', 'i4'],
    't500': ['i1', 'i3'],
    't600': ['i2', 'i3'],
    't700': ['i1', 'i3'],
    't800': ['i1', 'i2','i3','i5'],
    't900': ['i1','i2','i3']
}
item = ('i1','i2','i3','i4','i5')
L = {} # Tap pho bien, dictionary trong dictionary co dang {'k': dictionary}
minsup = 2

# Tim L1
def find_frequent_1itemset(item, minsup, T):
    '''
    Tim tap pho bien 1-itemset
    :param item: Tap cac item
    :param minsup: Nguong support
    :param T: Co so du lieu
    :return: Tap pho bien 1-itemset, dictionary
    '''
    L1 = []
    for i in item:
        count = 0
        for _,values in T.items():
            if i in values:
                count += 1
        if count >= minsup:
            L1.append((i,count))
    return L1
L1 = find_frequent_1itemset(item,minsup,T)
L['1'] = L1

# Sap xep L1
def sort(L1):
    size = len(L1)
    for i in range(0,size - 1):
        for j in range(i + 1, size):
            if L1[i][1] < L1[j][1]:
                temp = L1[i]
                L1[i] = L1[j]
                L1[j] = temp
    return L1
L1 = sort(L1)
print(L1)


# Lop Node
class Node:
    def __init__(self,key,value = 1,parent = None,headNode = None):
        self.key = key
        self.value = value
        self.parent = parent
        self.headNode = headNode
        self.Node_list = []
    def append(self,newNode):
        self.Node_list.append(newNode)
    def item(self):
        return (self.key,self.value)
    def __str__(self):
        rep = self.key + ':' + str(self.value) + '\n'
        if self.parent is not None:
            rep += '\tParent: ' + self.parent.key + str(self.parent.value) + '\n'
        else:
            rep += '\tParent: None\n'
        if self.headNode is not None:
            rep += '\theadNode: ' + self.headNode.key + str(self.headNode.value) + '\n'
        else:
            rep += '\theadNode: None\n'
        rep += '\t' + "Node list: "
        for i in self.Node_list:
            item = i.item()
            rep += '(' + item[0] + ':' + str(item[1]) + ')' + ','
        rep = rep[:-1]
        return rep
    def __eq__(self, other):
        if self.key == other.key:
            return True
        return False
    def isChild(self, item):
        '''Kiem tra chuoi item co xuat hien trong Node_list chua
        Hay la kiem tra nut con'''
        for i in self.Node_list:
            if item == i.key:
                return True
        return False
    def getNode(self,item):
        for i in self.Node_list:
            if item == i.key:
                return i
        return None
    def increase(self,item):
        '''Tang value len 1 don vi'''
        for i in self.Node_list:
            if item == i.key:
                i.value += 1

# Tao bang head
def create_HeaderTable(L1):
    header_table = []
    for i in L1:
        temp = Node(i[0],i[1],None,None)
        header_table.append(temp)
    return header_table
header_table = create_HeaderTable(L1)
# print("Header Table:")
# for i in header_table:
#     print(i)

# Tao nut goc
root = Node('root',1,None,None)
#print(root)


# Tao cay FP
def frequent_item(L1):
    '''Ham de tim chuoi frequent list trong L1'''
    frequent = []
    for i in L1:
        frequent.append(i[0])
    return frequent
frequent_list = frequent_item(L1)
print("Frequent list: ",frequent_list)
def insert_HeadTable(root:Node, node:Node):
    if root.headNode is None:
        root.headNode = node
    else:
        temp = root.headNode # Di toi node tiep theo
        insert_HeadTable(temp,node)
def insert_Tree(root:Node,header_table:list,frequent_trans:list):
    '''
    Chen vao cay tai nut goc
    :param root: Nut goc
    :param header_table: Bang head table
    :param frequent_trans: Chuoi pho bien cua transaction
    :return:
    '''
    if len(frequent_trans) == 0: # Neu chuoi frequent_trans khong con phan tu nao thi dung
        return
    first_item = frequent_trans[0]
    remaining_item = frequent_trans[1:]
    if root.isChild(first_item) == False: # Neu first_item khong la con cua root
        newNode = Node(first_item,1,root,None) # Tao node moi
        for i in header_table: # Them vao bang head tai phan tu i
            if newNode == i:
                insert_HeadTable(i,newNode)
                break
        root.append(newNode)
        temp = newNode
        insert_Tree(temp,header_table,remaining_item)
    else: # Neu first_item la con cua root
        root.increase(first_item)
        temp = root.getNode(first_item)
        insert_Tree(temp,header_table,remaining_item)
def create_FPTree(T, frequent_list, header_table, root):
    # Tim frequent item trong transaction va duoc sap xep theo thu tu nhu frequent_string
    for _,value in T.items(): # Duyet tung transaction
        frequent_trans = []
        for i in frequent_list:
            if i in value:
                frequent_trans.append(i)
        insert_Tree(root,header_table,frequent_trans)
    return root

# Chay thuat toan tao cay
root = create_FPTree(T,frequent_list,header_table,root)

# Ham in ket qua
def HT_print(root:Node):
    rep = '(' + root.key + ':' + str(root.value) + ')'
    rep += "-->"
    print(rep,end='')
    if root.headNode is not None:
        HT_print(root.headNode)
    else:
        print(" None")
def HeadTable_print(header_table:list):
    for i in header_table:
        HT_print(i)
def FPTree_print(root:Node,tab = 1):
    for i in range(0,tab):
        print('\t|',end='')
    rep = root.key + ': ' + str(root.value)
    print(rep)
    for i in root.Node_list:
        FPTree_print(i,tab + 1)

# In ket qua
print("HeaderTable la: ")
HeadTable_print(header_table)
print("Cay FP la: ")
FPTree_print(root,1)


# Khai thac tap pho bien
def discover_path(temp:list, root:Node,value:int):
    if root.key == 'root':
        return
    temp.append((root.key,value))
    parent = root.parent
    discover_path(temp,parent,value)
def FP_Growth(FP_Tree:Node,header_table:list, beta:str, minsup):
    conditional_PB = []
    for i in header_table:
        if i.key == beta:
            alpha = i.headNode
            while alpha is not None:
                temp = []
                discover_path(temp,alpha.parent,alpha.value)
                temp.reverse()
                if len(temp) != 0:
                    conditional_PB.append(temp)
                alpha = alpha.headNode
            break
    print(conditional_PB)
    size_CPB = len(conditional_PB)
    for i in range(0,size_CPB - 1):
        for j in range(i + 1, size_CPB):
            p1 = conditional_PB[i] # List 1
            p2 = conditional_PB[j] # List 2
            size = min(len(p1),len(p2))
            for k in range(0,size):
                if p1[k][0] == p2[0][0]: # Kiem tra id co bang nhau hay khong
                    p1[k] = (p1[k][0],p1[k][1] + p2[k][1])
                    p2.__delitem__(0)
                    size = min(len(p1), len(p2))
                    k -= 1

    # Xoa cac phan tu be hon minsup
    for i in range(0,size_CPB):
        for item in conditional_PB[i]:
            if item[1] < minsup:
                conditional_PB[i].remove(item)
        if len(conditional_PB[i]) == 0:
            conditional_PB.remove(conditional_PB[i])
    print(conditional_PB)
FP_Growth(root,header_table,'i5',2)

