import math
def min_max():
    input = open("plants.csv","r")
    state = {}
    head = input.readline() # Lấy header
    state_list = head.strip().split(',') # Lấy danh sách tên state
    print(state_list)
    print("len of state_list: ",len(state_list))
    for i in range(1,len(state_list)):
        state[state_list[i]] = 0
    print(state)
    print("Dang dem ...")
    stop = False
    for line in input:
        '''
        Lập cho từng dòng dữ liệu
        '''
        line = line.strip().split(',')
        if stop == False:
            print(line)
            print("len of line: ",len(line))
            stop = True
        for i in range(1,len(line)):
            '''
            Lập cho từng state của mỗi dòng dữ liệu'''
            if line[i] == 'y':
                '''Nếu có xuất hiện thì tăng key trong state'''
                state[state_list[i]] += 1

    print("Dem xong!")
    print(state)
    min_state = ''
    max_state = ''
    min = math.inf
    max = -math.inf
    sum = 0
    for states,values in state.items():
        sum += values
        if values <= min:
            min = values
            min_state = states
        if values >= max:
            max = values
            max_state = states
    print("min_state: ",min_state,"with ",min,"instance","and proportion is",min / 34781 * 100)
    print("max_state: ", max_state, "with ", max, "instances","and proportion is",max / 34781 * 100)
    print("average: ",sum / 69)
    input.close()

min_max()