def changeValue():
    '''
    Thay doi gia tri 'n' thanh '?'
    '''
    input = open("plants.csv","r")
    output = open("plants_changed.csv","w")
    head = input.readline()
    print("Dang ghi ...")
    output.write(head)
    for line in input:
        line = line.strip().split(',')
        line_changed = ''
        for i in range(0,len(line)):
            if line[i] == 'n':
                line[i] = '?'
            line_changed += line[i] + ','
        line_changed = line_changed[:-1]
        line_changed += '\n'
        output.write(line_changed)

    print("Da ghi xong!")
    output.close()
    input.close()

changeValue()