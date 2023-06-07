import sys
register={'000':'R0','001':'R1','010':'R2','011':'R3','100':'R4','101':'R5','110':'R6','111':'FLAGS'}
reg=[0,0,0,0,0,0,0,'0000000000000000']
def binarytodecimal(n):
    n=int(n)
    deci = 0
    exponent = 1
    while n>0:
        rem = n%10
        n = n//10
        deci += rem*exponent
        exponent = exponent*2
    return deci 
def decimaltobinary(n):
    n=int(n)
    a = ''
    while n > 0:
        a = str(n % 2) + a
        n //= 2
    a = '0'*(7-len(a)) + a
    return a
def decimaltobinary16(n):
    n=int(n)
    a = ''
    while n > 0:
        a = str(n % 2) + a
        n //= 2
    a = '0'*(16-len(a)) + a
    return a
flagis=True
binary_code=[]
MEM_d=[]
MEM_dump=[]
Trace=[]
binary=sys.stdin.readlines()
for line in binary:
        word=line.split()
        binary_code.append(word)
def PC(x):
    y=decimaltobinary(x)
    return str(y)
def MEM(x):
    MEM_dump.append(x)
def resetflagReg():
        flag = "0000000000000000"
        reg[7]=flag

def overflowflag():
        flag = "0000000000001000"
        reg[7]=flag
def lessthanflag(x):
    flag = "0000000000000100"
    reg[7]=flag
def greaterthanflag():
    flag = "0000000000000010"
    reg[7]=flag
def equalsflag():
    flag = "0000000000000001"
    reg[7]=flag
    
halted = False
pc=0
# print(binary)
while (not halted):
    instruction=binary[pc]
    opcode=instruction[0:5]
    if(opcode=='00000'):
        #Add instruction type-A
        rx=instruction[7:10]
        reg1=binarytodecimal(rx)
        reg2=binarytodecimal(instruction[10:13])##reg2=2(index)
        reg3=binarytodecimal(instruction[13::])
        if (reg[reg2]+reg[reg3]>65536) or (reg[reg2]+reg[reg3]<0):
            overflowflag()
            reg[binarytodecimal(int(rx))]=0
        else:
            reg[reg1]=reg[reg2]+reg[reg3]
    elif(opcode=='00001'):
        #Sub instruction type-A
        rx=instruction[7:10]
        reg1=binarytodecimal(rx)
        reg2=binarytodecimal(instruction[10:13])##reg2=2(index)
        reg3=binarytodecimal(instruction[13::])
        if (reg[reg3]>reg[reg2]) or (reg[reg2]-reg[reg3]<0):
            overflowflag()
            reg[binarytodecimal(register.get(rx))]=0
        else:
            resetflagReg()
    elif(opcode=='00010'):
            #MovImm instruction type-B
            reg1=instruction[6:9]##reg2=010
            imm=instruction[9::]
            reg[binarytodecimal(int(reg1))]=binarytodecimal(imm)
            resetflagReg()
    elif(opcode=='00011'):
            #Movreg instruction type-C
            reg1=instruction[10:13]
            reg2=instruction[13::]
            reg[binarytodecimal(int(reg1))]=reg[binarytodecimal(int(reg2))]
            resetflagReg()
    elif(opcode=='00100'):
            #Load instruction type-d
            reg1=instruction[6:9]
            mem_add=instruction[9::]
            resetflagReg()
    elif(opcode=='00101'):
            #Store instruction type-d
            reg1=binarytodecimal(instruction[6:9])
            mem_add=instruction[9::]
            MEM_d.append(decimaltobinary16(reg[reg1]))
            resetflagReg()
            # print("hello")
    elif(opcode=='00110'):
            #Mul instruction type-A
        rx=instruction[7:10]
        reg1=binarytodecimal(rx)
        reg2=binarytodecimal(instruction[10:13])##reg2=2(index)
        reg3=binarytodecimal(instruction[13::])
        if (reg[reg3]*reg[reg2]>65536) or (reg[reg2]*reg[reg3]<0):
            overflowflag()
            reg[reg1]=0
        else:
            resetflagReg()
    elif(opcode=='00111'):
            #Div instruction type-C
            reg1=instruction[10:13]
            reg2=instruction[13::]
            if reg2==0:
                overflowflag()
                reg['R0']=0
                reg['R1']=0
            else:
                reg['R0']=reg1//reg2
                reg['R1']=reg1%reg2
            resetflagReg()
    elif(opcode=='01000'):
            #RShift instruction type-b
            reg1=instruction[6:9]
            r1=binarytodecimal(int(reg1))
            imm=instruction[9::]
            reg[binarytodecimal(int(reg1))]=r1>>imm
            resetflagReg()
    elif(opcode=='01001'):
            #LShift instruction type-b
            reg1=instruction[6:9]
            r1=binarytodecimal(int(reg1))
            imm=instruction[9::]
            reg[binarytodecimal(int(reg1))]=r1<<imm
            resetflagReg()
    elif(opcode=='01010'):
            #Xor instruction type-A
            rx=instruction[7:10]
            reg1=binarytodecimal(rx)
            reg2=binarytodecimal(instruction[10:13])##reg1=2(index)
            reg3=binarytodecimal(instruction[13::])
            x=reg[reg1]^reg[reg2]
            reg[binarytodecimal(register.get(rx))]=0
            resetflagReg()
    elif(opcode=='01011'):
            #Or instruction type-A
            rx=instruction[7:10]
            reg1=binarytodecimal(rx)##reg1=2(index)
            reg2=reg[binarytodecimal(instruction[10:13])]
            reg3=reg[binarytodecimal(instruction[13::])]
            r1=reg2|reg3
            reg[reg1]=r1
            resetflagReg()
    elif(opcode=='01100'):
            #And instruction type-A
            rx=instruction[7:10]
            reg1=binarytodecimal(rx)##reg1=2(index)
            reg2=reg[binarytodecimal(instruction[10:13])]
            reg3=reg[binarytodecimal(instruction[13::])]
            r1=reg2&reg3
            reg[reg1]=r1
            resetflagReg()
    elif(opcode=='01101'):
            #Invert instruction type-C
            reg1=binarytodecimal(int(instruction[10:13]))#reg1=2(index)
            reg2=reg[binarytodecimal(int(instruction[13::]))]
            r1=~reg2
            reg[reg1]=r1
            resetflagReg()
    elif(opcode=='01110'):
            #Cmp instruction type-c
            r1=binarytodecimal(int(instruction[10:13]))
            r2=binarytodecimal(int(instruction[13::]))
            reg1=reg[r1]
            reg2=reg[r2]
            if int(reg1)<int(reg2):
                lessthanflag()
            elif int(reg1)>int(reg2):
                greaterthanflag()
            else:
                equalsflag()
    elif(opcode=='01111'):
            #Jump instruction  type-E
            # print("jump",pc)
            mem_add1=binarytodecimal(int(instruction[9::]))
            flagis=False
            temp=mem_add1-1
            resetflagReg()
    elif(opcode=='11100'):
            #JumpIfLessThan instruction type-E
        mem_add1=binarytodecimal(int(instruction[9::]))
        if reg[7]== "0000000000000100":
            # print("this less",pc)
            temp=mem_add1-1
            flagis=False
            resetflagReg()
        else:
            resetflagReg()
    elif(opcode=='11101'):
            #JumpIfGreaterThan instruction type-E
        mem_add1=binarytodecimal(instruction[9::])
        if reg[7]== "0000000000000010":
            # print("this greater",pc)
            # print(instruction)
            # print("memory",mem_add1)
            temp=mem_add1-1
            # print("this greater",pc)
            resetflagReg()
            flagis=False
        else:
            resetflagReg()
    elif(opcode=='11111'):
            #JumpIfEqual instruction type-E
        mem_add1=binarytodecimal(instruction[9::])
        if reg[7]== "0000000000000001":
            # print("this equal",pc)
            temp=mem_add1-1
            flagis=False
            resetflagReg()
        else:
            resetflagReg()
        
    elif(opcode=='11010'):
            #Halt instruction type-F
            halted =False
            resetflagReg()
    Trace.append(decimaltobinary(pc)+8*" "+str(decimaltobinary16(reg[0])) +' '+str(decimaltobinary16(reg[1]))+' '+str(decimaltobinary16(reg[2])) +' '+str(decimaltobinary16(reg[3])) +' '+str(decimaltobinary16(reg[4]))+' '+str(decimaltobinary16(reg[5])) +' '+str(decimaltobinary16(reg[6]))+' '+str(reg[7])+'\n')
    if flagis==False:
        pc=temp
        flagis=True
    pc+=1
    # print(pc)
    # print(opcode)
    if(opcode=='11010'):
            #Halt instruction type-F
            halted =False
            break
            resetflagReg()
for i in binary_code:
    MEM_dump.append(i[0])
for i in MEM_d:
    MEM_dump.append(i)
for i in range(128-len(MEM_dump)):
    MEM_dump.append(decimaltobinary16(0))
x=1
for i in Trace:
        # sys.stdout.write(str(x))
        sys.stdout.write(i)
        # x+=1
for i in MEM_dump:
    sys.stdout.write(i)
    # sys.stdout.write(str(x))
    sys.stdout.write("\n")
    # x+=1