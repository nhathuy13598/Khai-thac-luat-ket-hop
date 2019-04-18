T = {
    "100": ['I', 'B', 'F', 'D', 'E', 'C', 'H', 'J'],
    "200": ['F', 'G', 'A', 'D', 'C'],
    "300": ['B', 'J', 'D', 'A', 'H'],
    "400": ['A', 'B', 'E', 'G']
}
item = ('A','B','C','D','E','F','G','H','I','J')
L = {} # Tap pho bien, dictionary trong dictionary co dang {'k': dictionary}
minsup = 2
def find_frequent_1itemset(item, minsup, T):
    '''
    Tim tap pho bien 1-itemset
    :param item: Tap cac item
    :param minsup: Nguong support
    :param T: Co so du lieu
    :return: Tap pho bien 1-itemset, dictionary
    '''
    L1 = {}
    for i in item:
        count = 0
        for _,values in T.items():
            if i in values:
                count += 1
        if count >= minsup:
            L1[i] = count
    return L1
L1 = find_frequent_1itemset(item,minsup,T)
L['1'] = L1
#print(L)
def generate_subset(set,origin_id:str, id:str, index, size):
    if len(id) == size:
        set.append(id)
        return
    for c in range(index,len(origin_id)):
        if origin_id[c] not in id:
            id += origin_id[c]
            generate_subset(set,origin_id, id, c + 1, size)
            id = id[:-1]

def has_infrequent_subset(id:str, L_ksub1:dict):
    '''
    Kiem tra xem cac subset cua id co thuoc L_ksub1 hay khong
    Ta se tao cac subset cua id bang ham generate_subset
    :param id: Day cac ten item
    :param L_ksub1: Cac frequent (k-1) itemset
    :return: True neu co tap khong pho bien trong id, False neu khong ton tai tap khong pho bien trong d
    '''
    subset = []
    size = len(id) - 1
    generate_subset(subset, id, '', 0, size)
    for i in subset:
        if i not in L_ksub1.keys():
            return True
    return False

def Apriori_gen(L_ksub1:dict):
    '''
    Tao tap ung vien k-itemset tu tap L(k-1)
    :param L_ksub1: Tap L(k-1), dictionary co dang {'item_ids': count}
    :return: Tap ung vien, dictionary
    '''
    C_k = {} # Tap ung vien, dictionary co dang {'item_ids': count}
    for id1 in L_ksub1.keys():
        for id2 in L_ksub1.keys():
            if id1[:-1] == id2[:-1] and id1[-1] != id2[-1]:
                if id1[-1] < id2[-1]:
                    id = id1 + id2[-1]
                else:
                    id = id2 + id1[-1]
                if id not in C_k:
                    if has_infrequent_subset(id,L_ksub1) == False:
                        '''Kiem tra xem trong id co tap khong pho bien hay khong'''
                        C_k[id] = 0 # Neu khong co ta se them vao tap ung vien C_k
    return C_k


def Apriori_Run(T,L,minsup):
    '''
    Chay thuat toan Apriori
    :param T: Co so du lieu
    :param L: Tap cac k-itemset, dictionary trong dictionary co dang {'k': {}}
    :param minsup: minimum support
    :return: L
    '''
    k = 2
    while len(L[str(k - 1)]) != 0:
        '''Khi tap k-itemset khac rong thi ta chay thuat toan'''
        k_itemset = Apriori_gen(L[str(k-1)])
        if len(k_itemset) == 0:
            break
        temp_kitemset = k_itemset.copy()
        for key,value in k_itemset.items():
            '''Xet tung ung vien trong k-itemset'''
            count = 0
            for _,item in T.items():
                '''Xet tung transaction'''
                count += 1 # Gia su ung vien co xuat hien trong transaction
                for i in range(0,len(key)):
                    if key[i] not in item:
                        '''Neu ung vien that su khong xuat hien trong transaction thi giam count'''
                        count -= 1
                        break
            if count >= minsup:
                temp_kitemset[key] = minsup
            else:
                temp_kitemset.pop(key)
        k_itemset = temp_kitemset.copy()
        L[str(k)] = k_itemset
        k += 1
    return L

L = Apriori_Run(T,L,minsup)
print(L)