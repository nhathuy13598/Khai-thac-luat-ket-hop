import copy
def read_data(filename):
    data = open(filename, "r")
    item = data.readline()
    itemset = tuple(item.strip().split(','))
    transaction = {}
    id = 1
    for line in data:
        fLine = line.strip().split(',')
        transaction[id] = fLine
        id += 1
    data.close()
    return itemset,transaction

item,T = read_data('data.txt')

minsup = int(input("Nhap minsup: "))
minconf = int(input("Nhap minconf (0<= minconf <=1): "))

L = {} # Tap pho bien, dictionary trong dictionary co dang {'k': dictionary}

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
    def increase(self,item,increment):
        '''Tang value len 1 don vi'''
        for i in self.Node_list:
            if item == i.key:
                i.value += increment

# Tao bang head
def create_HeaderTable(L1):
    header_table = []
    for i in L1:
        temp = Node(i[0],i[1],None,None)
        header_table.append(temp)
    return header_table
header_table = create_HeaderTable(L1)

# Tao nut goc
root = Node('root',1,None,None)



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
    :param frequent_trans: Chuoi pho bien cua transaction, co dang list cua tuple ('id',count)
    :return:
    '''
    if len(frequent_trans) == 0: # Neu chuoi frequent_trans khong con phan tu nao thi dung
        return
    first_item = frequent_trans[0][0]
    remaining_item = frequent_trans[1:]
    if root.isChild(first_item) == False: # Neu first_item khong la con cua root
        newNode = Node(first_item,frequent_trans[0][1],root,None) # Tao node moi
        for i in header_table: # Them vao bang head tai phan tu i
            if newNode == i:
                insert_HeadTable(i,newNode)
                break
        root.append(newNode)
        temp = newNode
        insert_Tree(temp,header_table,remaining_item)
    else: # Neu first_item la con cua root
        root.increase(first_item,frequent_trans[0][1])
        temp = root.getNode(first_item)
        insert_Tree(temp,header_table,remaining_item)
def create_FPTree(T, frequent_list, header_table, root):
    # Tim frequent item trong transaction va duoc sap xep theo thu tu nhu frequent_string
    for _,value in T.items(): # Duyet tung transaction
        frequent_trans = []
        for i in frequent_list:
            if i in value:
                frequent_trans.append((i,1))
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
def Conditional_pattern(header_table:list, beta:str):
    # Tao Conditional Pattern Base
    conditional_PB = []
    MyNode = None
    for i in header_table:
        if i.key == beta:
            alpha = i.headNode
            MyNode = (i.key, i.value)
            while alpha is not None:
                temp = []
                discover_path(temp, alpha.parent, alpha.value)
                temp.reverse()
                if len(temp) != 0:
                    conditional_PB.append(temp)
                alpha = alpha.headNode
            break
    return conditional_PB
def FP_Growth(FP_Tree:Node,header_table:list,final_result,item_list,value_list, beta:str,value, minsup):

    item_templist = item_list.copy() # Danh sach chua cac item pho bien
    value_templist = value_list.copy() # Danh sach chua cac value
    item_templist.append(beta)
    value_templist.append(value)
    final_result.append((item_templist,min(value_templist)))
    conditional_PB = Conditional_pattern(header_table,beta)
    if len(conditional_PB) == 0:
        return


    # Tao frequent item cho Conditional_PB
    frequent_item_in_CPB = {}
    for i in conditional_PB: # i la list cua cac node, moi node la tuple
        for j in i: # Duyet tung node, moi node la tuple
            if j[0] not in frequent_item_in_CPB:
                frequent_item_in_CPB[j[0]] = j[1]
            else:
                frequent_item_in_CPB[j[0]] += j[1]
    for key in list(frequent_item_in_CPB.keys()):
        if frequent_item_in_CPB[key] < minsup:
            del frequent_item_in_CPB[key]
    sorted_frequent_item = [(k, frequent_item_in_CPB[k]) for k in sorted(frequent_item_in_CPB, key=frequent_item_in_CPB.get, reverse=True)]

    # Tao FP Tree
    size_CPB = len(conditional_PB)
    head_SubTable = []
    root = Node('root', 1, None, None)  # Tao nut goc
    for i in sorted_frequent_item:
        head_SubTable.append(Node(i[0],i[1]))

    # Tao frequent trans trong tung Conditional_FB
    for i in conditional_PB: # Duyet tung path
        frequent_trans = []
        for j in i: # Duyet tung node cua path
            for k in sorted_frequent_item:
                if j[0] == k[0]:
                    frequent_trans.append(j)
                    break
        insert_Tree(root,head_SubTable,frequent_trans)
    for i in head_SubTable:
        FP_Growth(root,head_SubTable,final_result,item_templist,value_templist,i.key,i.value,minsup)



def Run_FPGrowth(root,header_table,minsup):
    size = len(header_table) - 1
    final = []
    itemlist = []
    valuelist = []
    while size >= 0:
        FP_Growth(root,header_table,final,itemlist,valuelist,header_table[size].key,header_table[size].value,minsup)
        size -= 1
    return final

final = Run_FPGrowth(root,header_table,minsup)
print("Tap pho bien la: ",end='')
for item in final:
    print(item)