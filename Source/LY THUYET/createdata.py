import random
seq = 'ABCDEFGHIJKLMNOPQXYZT'
head = 'A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,X,Y,Z,T\n'
line = 3000
length = len(seq)   
file = open('data.txt',"w")
file.write(head)
for i in range(0,line): 
	random_str = ''
	for blah in range(len(seq) * 2): #Apologies for the lame variable names
	    x = random.randint(0,length - 1)
	    random_str += seq[x] + ','
	random_str = random_str[:-1] + '\n'
	file.write(random_str)
file.close()