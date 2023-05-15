import sys
opcode= {'add': '00000', 'sub': '00001', 'mov': '00010', 'ld': '00100', 'st': '00101', 'mul': '00110', 'div': '00111', 'rs': '01000', 'ls': '01001', 'xor': '01010', 'or': '01011', 'and': '01100', 'not': '01101', 'cmp': '01110', 'jmp': '01111', 'jlt': '11100', 'jgt': '11101', 'je': '11111', 'hlt': '11010'}
type_isa={'add':'A','sub':'A','mov':'B','ld':'D','st':'D','mul':'A','div':'C','rs':'B','ls':'B','xor':'A','or':'A','and':'A','not':'C','cmp':'C','jmp':'E','jlt':'E','jgt':'E','je':'E','hlt':'F'}
reg={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}
variables={}
labels={}
###converts the decimal to binary ###
def decimalToBinary(n):
    n=int(n)
    a = ''
    while n > 0:
        a = str(n % 2) + a
        n //= 2
    a = '0'*(7-len(a)) + a
    return a
###Function for diff encoding type which convert instructions to binary###
def type_A(l):
    try:
        a=opcode.get(l[0])
        r1=reg.get(l[1])
        r2=reg.get(l[2])
        r3=reg.get(l[3])
        str=a+'00'+r1+r2+r3
        return str
    except TypeError:
        print("Wrong register used")
        sys.exit()
def type_B(l):
    try:
        if l[0]=='mov' :
            a='00010'
        else:
            a=opcode.get(l[0])
        r1=reg.get(l[1])
        b=l[2].strip("$")
        str=a+"0"+r1+decimalToBinary(b)
        return str
    except TypeError:
        print("Wrong register used")
        sys.exit()
def type_C(l):
    try:
        if l[0]=='mov':
            a='00011'
        else:
            a=opcode.get(l[0])
        r1=reg.get(l[1])
        r2=reg.get(l[2])
        str=a+"00000"+r1+r2
        return str
    except TypeError:
        print("Wrong register used")
        sys.exit()
def type_D(l):
    try:
        a=opcode.get(l[0])
        r1=reg.get(l[1])
        memory_add=variables.get(l[2])
        str=a+"0"+r1+memory_add
        return str
    except TypeError:
        print("Wrong register or variable used")
        sys.exit()
def type_E(l):
    a=opcode.get(l[0])
    make_label_dict(l)
    memory_add=labels.get(l[1])
    str=a+"0000"+memory_add
    return str
def type_F(l):
    a=opcode.get(l[0])
    str=a+"00000000000"
    return str
def make_label_dict(l):
    for i in label_comm:
        new=i[0][0].strip(":")
        if new==l[1]:
            labels[l[1]]=decimalToBinary(i[1])
###file input and converts input in 2d list###
### calls the  functions for diff type of encoding and generates binary code ###
count=0
label_comm=[]
with open("test02.txt","r") as file:
    assembly_code=[]
    assembly=file.readlines()
    for line in assembly:
        word=line.split()
        if word!=[]:
            if word[0]=='var':
                variables[word[1]]=1
            elif word[0] in type_isa:    
                assembly_code.append(word)
                count+=1
            # elif word[0][0:5]=='label':
            #         l=[]
            #         for i in range(1,len(word)):
            #             l.append(word[i])
            #         assembly_code.append(l)
            #         label_comm.append((word,count))
            #         count+=1
            elif word[0][-1]==":":
                l2=[]
                for i in range(1,len(word)):
                    l2.append(word[i])
                assembly_code.append(l2)
                label_comm.append((word,count))
                count+=1

            # elif 1:
            #         new=word[0].strip(':')
            #         for j in assembly_code:
            #             if len(j)== 2 and j[1] == new:
            #                 labels[new]=decimalToBinary(count)
            #                 assembly_code.append([word[1]])
            #                 count+=1
            #                 break
            #         else:
            #             assembly_code.append(word)
            else:
                print("wrong")
for k in variables:
    variables[k]=decimalToBinary(count)
    count+=1
# print(assembly_code)
# print(len(assembly_code))
# print(variables)
# print(labels)
# print(label_comm)
for i in assembly_code:
        if i[0] in type_isa:
            if (type_isa[i[0]])=="A":
                # print("A")
                print(type_A(i),end="\n")
            elif (type_isa[i[0]])=="B":
                if i[0]=="mov":
                    if i[2] not in reg:
                        # print("B")
                        print(type_B(i),end="\n")
                    else:
                        # print("C")
                        print(type_C(i),end="\n")
            elif (type_isa[i[0]])=="C":
                # print("C")
                print(type_C(i),end="\n")
            elif (type_isa[i[0]])=="D":
                # print("D")
                print(type_D(i),end="\n")
            elif (type_isa[i[0]])=="E":
                # print("E")
                print(type_E(i),end="\n")
            elif (type_isa[i[0]])=="F":
                # print("F")
                print(type_F(i),end="\n")
        else:
            if i[0] not in type_isa:
                print("Wrong Opcode")
            sys.exit()
            # break