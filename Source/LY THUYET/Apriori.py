import time
def read_data(filename):
    '''
    Đọc dữ liệu trong file
    :param filename: Đường dẫn đến file
    :return: Tập tên các item, Transaction
    '''
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
print("Tap pho bien la: \n")
for i in L.values():
    print(i)

def association_rule(frequent_set:dict,L:dict, minconf:int):
    '''
    Liet ke cac luat ket hop thoa minconf
    :param L: Tap pho bien
    :return:
    '''
    for k in range(2,len(L)):
        '''Tim luat ket hop tu 2 tap 2 item tro len'''
        k_itemset = frequent_set[str(k)] # Tap cac k-item pho bien, dictionary co dang {'item_id': count}
        for items,value in k_itemset.items(): # Lay item_id va count
            for size in range(1,len(items)): # Lap theo kich thuoc cua item_id
                subset = [] # Mang luu cac tap con
                generate_subset(subset,items,'',0,size) # Tao subset
                for i in subset: # Lap voi moi tap trong subset, i ung voi ve sau cua menh de Neu ... thi ...
                    newStr = items
                    for charac in i: # Tao phan Neu ...
                        newStr = newStr.replace(charac,'')
                    newsize = len(newStr) # Lay kich thuoc cua phan neu
                    if value / L[str(newsize)][newStr] >= minconf: # Tinh conf
                        print(newStr,'=>',i,'with conf',value / L[str(newsize)][newStr]*100,"%")
print("\tLuat khai thac bang tap pho bien la:")
start = time.time()
association_rule(L,L,1)
end = time.time()
print("Time for frequent items: ",end - start)

def Close_Frequent_item(L:dict):
    Closed_L = {}
    Closed_L['1'] = L['1']
    for k in range(2,len(L) + 1): # Lap tu tap 2-itemset
        Closed_L[str(k)] = {}
        for kitem in  L[str(k)].items(): # Voi moi item trong k-itemset
            isClosed = True
            for j in range(k + 1,len(L) + 1): # Lap tu tap 3-itemset tro len
                for jitem in L[str(j)].items(): # Voi moi item trong (k+1)-itemset
                    if kitem[1] == jitem[1]:
                        size = len(kitem[0])
                        count = 0
                        for character in kitem[0]:
                            if character in jitem[0]:
                                count += 1
                        if count == size:
                            isClosed = False
                            break
            if isClosed == True:
                Closed_L[str(k)][kitem[0]] = kitem[1]
    return Closed_L
Closed_L = Close_Frequent_item(L)
print("Tap pho bien dong la: \n")
for i in Closed_L.values():
    print(i)
print("\tLuat khai thac bang tap pho bien dong:")
start = time.time()
association_rule(Closed_L,L,1)
end = time.time()
print("Time for closed frequent items: ",end - start)

def Maximax_Frequent_item(Closed_L):
    Maximax_L = {}
    Maximax_L['1'] = Closed_L['1']
    for k in range(2,len(Closed_L) + 1): # Lap tu tap 2-itemset
        Maximax_L[str(k)] = {}
        for kitem in  Closed_L[str(k)].items(): # Voi moi item trong k-itemset
            isMaximax = True
            for j in range(k + 1,len(Closed_L) + 1): # Lap tu tap 3-itemset tro len
                for jitem in Closed_L[str(j)].items(): # Voi moi item trong (k+1)-itemset
                    if kitem[1] <= jitem[1]:
                        size = len(kitem[0])
                        count = 0
                        for character in kitem[0]:
                            if character in jitem[0]:
                                count += 1
                        if count == size:
                            isMaximax = False
                            break
            if isMaximax == True:
                Maximax_L[str(k)][kitem[0]] = kitem[1]
    return Maximax_L
Maxima_L = Maximax_Frequent_item(L)
print("Tap pho bien toi dai la: \n")
for i in Maxima_L.values():
    print(i)
print("\tLuat khai thac bang tap pho bien toi dai:")
start = time.time()
association_rule(Maxima_L,L,1)
end = time.time()
print("Time for maxima frequent items: ",end - start)