def get_state():
    dict = {}
    file = open("stateabbr_process.txt",'r')
    for line in file:
        state = line.strip().split(' ',maxsplit = 1)
        state = state[0]
        dict[state] = "n"
    file.close()
    print(dict)
    return dict
state = get_state()
def convert():
    file_in = open("plants.data","r")
    file_out = open("plants.csv","w")
    head = 'name,'
    for key in state.keys():
        head += key + ','
    head = head[:-1]
    head += '\n'
    file_out.write(head)
    for line in file_in:
        list = line.strip().split(',')
        temp_state = state.copy()
        for i in range(1,len(list)):
            if list[i] in temp_state:
                temp_state[list[i]] = 'y'
        str_for_write = list[0] + ','

        for _,value in temp_state.items():
            str_for_write += value + ','
        str_for_write = str_for_write[:-1]
        str_for_write += '\n'
        file_out.write(str_for_write)
    file_in.close()
    file_out.close()
print("Dang chuyen ...")
convert()
print("Xong")