# Có trọng số
# T = {
#     "100": ['I', 'B', 'F', 'D', 'E', 'C', 'H', 'J'],
#     "200": ['F', 'C', 'F', 'G', 'A', 'D', 'C'],
#     "300": ['B', 'J', 'D', 'A', 'H'],
#     "400": ['E', 'A', 'B', 'E', 'G']
# }
# Không có trọng số
T = {
    "100": ['I', 'B', 'F', 'D', 'E', 'C', 'H', 'J'],
    "200": ['F', 'G', 'A', 'D', 'C'],
    "300": ['B', 'J', 'D', 'A', 'H'],
    "400": ['A', 'B', 'E', 'G']
}
item = ('A','B','C','D','E','F','G','H','I','J')
minsup = 2
large_item = [] # Mảng lưu các items có số lần xuất hiện lớn hơn minsup
# Làm lần đầu tiên
def appear_first(T,x):
    sum = 0
    item_set = []
    for id in T:
        # Có trọng số
        #sum += T[id].count(x)
        # Không có trọng số
        if x in T[id]:
            sum += 1
    if sum < minsup:
        return -1
    item_set.append(x)
    return (item_set,sum)

for x in item:
    tup = appear_first(T,x)
    if tup != -1:
        large_item.append(tup)
print("Large item ban dau la: ")
print(large_item)

# Làm cho các tập large_set lớn hơn
'''
@ appear
:param T: Bảng dữ liệu
:param x: Danh sách của các item cần xét
:return: Trả về tuple gồm danh sách của item và số lượng xuất hiện
'''
def appear(T,x):
    sum = 0 # Biến lưu số lượng các transaction mà tập item xuất hiện

    # Duyệt từng transaction trong T
    for id in T:
        '''
        Đoạn này có trọng số
        # sum_item = []  # Mảng lưu số lần xuất hiện của các item trong 1 transaction
        # 
        # # Duyệt từng item trong x và đếm số lần xuất hiện hiện của từng item
        # # trong 1 transaction
        # for index in range(len(x)):
        #     if x[index] not in T[id]: # Nếu item không xuất hiện trong transaction thứ i thì ta break
        #         break
        # 
        #     # Nếu item đó xuất hiện thì ta đếm số lần xuất hiện của nó trong transaction thứ i
        #     count_item = T[id].count(x[index])
        # 
        #     # Thêm vào mảng sum_item
        #     sum_item.append(count_item)
        # 
        # # Vì transaction có thể không chứa x nên ta phải kiểm tra sum_item không được rỗng
        # # Tăng biến
        # if sum_item != []:
        #     sum += min(sum_item)
        '''
        contain = True # x nằm trong T[id]
        for index in range(len(x)):
            if x[index] not in T[id]:
                contain = False
                break
        if contain == True:
            sum += 1
    if sum < 2:
        return -1
    return (x,sum)

change = True # Biến kiểm tra xem trong 1 lần chạy large_item có thay đổi hay không nếu không thay đổi thì dừng
length = 1 # Biến xác định số lượng item

# Duyệt tất cả các trường hợp
while change == True:
    change = False
    '''
    Duyệt từng item trong large_item
    Mỗi phân tử trong large_item là một tuple
    x có dạng như sau (item,sum)
    item: là tập các item
    sum: là số lượng item đó xuất hiện
    '''
    size = len(large_item)

    for i in range(size):
        x = large_item[i] # Tập item 1

        if len(x[0]) == length: # Kiểm tra xem số lượng item có bằng length hay không
            for j in range(i + 1,size):
                y = large_item[j] # Tập item 2

                if len(y[0]) == length:
                    for k in range(len(y[0])):
                        if y[0][k] not in x[0]:
                            print("y[0][k] là: ", y[0][k])
                            print("x[0] + list(y[0][k]) là: ",x[0] + list(y[0][k]))
                            tup = appear(T,x[0] + list(y[0][k]))

                            if tup != -1:
                                large_item.append(tup)
                                change = True
    length += 1
print("Large item luc sau la: ")
#print(large_item)
size = len(large_item)
i = 0
while i < size - 1:
    j = i + 1
    while j >= i + 1 and j < size:
        flag = True
        if all(x in large_item[i][0] for x in large_item[j][0]):
            large_item.__delitem__(j)
            size -= 1
            j -= 1
        j += 1
    i += 1

print(large_item)