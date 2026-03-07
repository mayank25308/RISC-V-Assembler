
registers={"x0":"00000","x1":"00001","x2":"00010","x3":"00011","x4":"00100",
           "x5":"00101","x6":"00110","x7":"00111","x8":"01000","x9":"01001",
           "x10":"01010","x11":"01011","x12":"01100","x13":"01101","x14":"01110",
           "x15":"01111","x16":"10000","x17":"10001","x18":"10010","x19":"10011",
           "x20":"10100","x21":"10101","x22":"10110","x23":"10111","x24":"11000",
           "x25":"11001","x26":"11010","x27":"11011","x28":"11100","x29":"11101",
           "x30":"11110","x31":"11111","zero":"00000","ra":"00001",
           "sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110",
           "t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010",
           "a1":"01011","a2":"01100","a3":"01101","a4":"01110","a5":"01111",
           "a6":"10000","a7":"10001","s2":"10010","s3":"10011","s4":"10100",
           "s5":"10101","s6":"10110","s7":"10111","s8":"11000","s9":"11001",
           "s10":"11010","s11":"11011","t3":"11100","t4":"11101","t5":"11110",
           "t6":"11111"
            }



Rtype={"add":{"opcode":"0110011","func3":"000","func7":"0000000"},
       "sub":{"opcode":"0110011","func3":"000","func7":"0100000"},
       "sll":{"opcode":"0110011","func3":"001","func7":"0000000"},
       "slt":{"opcode":"0110011","func3":"010","func7":"0000000"},
       "sltu":{"opcode":"0110011","func3":"011","func7":"0000000"},
       "xor":{"opcode":"0110011","func3":"100","func7":"0000000"},
       "srl":{"opcode":"0110011","func3":"101","func7":"0000000"},
       "or":{"opcode":"0110011","func3":"110","func7":"0000000"},
       "and":{"opcode":"0110011","func3":"111","func7":"0000000"}}

Itype={"addi":{"opcode":"0010011","func3":"000"},
       "sltiu":{"opcode":"0010011","func3":"011"},
       "lw":{"opcode":"0000011","func3":"010"},
       "jalr":{"opcode":"1100111","func3":"000"}}

Btype={"beq":{"opcode":"1100011","func3":"000"},
       "bne":{"opcode":"1100011","func3":"001"},
       "bgeu":{"opcode":"1100011","func3":"111"},
       "blt":{"opcode":"1100011","func3":"100"},
       "bge":{"opcode":"1100011","func3":"101"},
       "bltu":{"opcode":"1100011","func3":"110"}}

Jtype={"jal":{"opcode":"1101111"}}



# this function will read the input filr and store the instructions in a list
def read_file(file):
    try:
        with open(file,'r') as f:
            info=f.readlines()
        lines=[]
        for i in info:
            i=i.split('#')[0].strip() #this removes the comments
            if i:           # '' is skipped here
                lines.append(i)
        return(lines)
    
    except FileNotFoundError:
        print("file not found")
        return []

read_file("input.txt")


def split_part(line):

    # to remove the label part i did this 

    if ":" in line:
        line= line.split(':', 1)[1]
    
    line=line.replace(',',' ')
    line=line.replace('(',' ').replace(')',' ')
    
   
    line=line.strip() #to remove extra spaces at begening
   
    line=line.split()

    return(line)


def labelmap_and_lines(lines):
    label_map={}
    c_line=[]
    position=0
    for i in lines:
        if ":" not in i:
            c_line.append(i)
            position+=4
        else:
            part= i.split(':', 1 )
            first=part[0].strip()
            second=part[1].strip()

            label_map[first]=position

            if second:
                c_line.append(second)
                position+=4
    
    return label_map,c_line


def encode_r(parts):
    
    if len(parts)!=4:
        print("wrong number of arguments")
        exit()
    instr = parts[0]
    if instr not in Rtype:
        print("invalid instruction")

    if parts[1] not in registers:
        print( "invalid parameter" + parts[1])
        exit()

    if parts[2] not in registers:
        print( "invalid parameter" + parts[2])
        exit()

    if parts[3] not in registers:
        print( "invalid parameter" + parts[3])
        exit()

    rd = registers[parts[1]]
    r1 = registers[parts[2]]
    r2 = registers[parts[3]]

    opcode=Rtype[instr]["opcode"]
    func3=Rtype[instr]["func3"]
    func7=Rtype[instr]["func7"]

    return func7 + r2 + r1 + func3 + rd + opcode


def to_binary(number, bits):
    if number < 0:
        number = (2**bits) + number
    
    result = ""

    for i in range(bits - 1, -1, -1):
        bit = (number >> i) & 1
        result += str(bit)
    return result  


def encode_i(parts,label_map,addr):
    return "00"
   
def encode_b(parts,label_map,addr):
    return "00000000000000000000000001100011"
    

def encode_s(parts):
    print("enter you code here for stype")

def encode_j(parts,label_map,addr):
    print("enter you code here for jtype")


def gen_machine_code(c_line,label_map):

    b_output=[]
    error_list=[]
    addr=0

    s_seen= False
    s_last = False


    for i in c_line:
        parts= split_part(i)
        print("processing", parts)

        if not parts:
            continue
        inst=parts[0]
        if inst in Rtype:
            result = encode_r(parts)
            s_last= False

        elif inst in Itype:
            result= encode_i(parts,label_map,addr)
            s_last= False
        elif inst in Btype:
            result = encode_b(parts,label_map,addr)
            
            if parts == ["beq","zero","zero","0"]:
                s_seen= True
                s_last= True
            else:
                s_last= False

        elif inst == "sw":

            result = encode_s(parts)

            s_last= False

        elif inst in Jtype:

            result = encode_j(parts,label_map, addr)

            s_last = False
        else:
            result = None
            err= "unknonwn instruction" + inst
            s_last = False
        
        addr+=4
        b_output.append(result)
    
    if not s_seen:
        print("Error: missing virtual halt ")
        exit()

    if not s_last:
        print("Error: virtual halt is not the last instruction ")
        exit()


    return b_output, error_list


import sys

file= "input.txt"
output_file= "output.txt"

lines = read_file(file)
label_map, c_line = labelmap_and_lines(lines)
b_output, error_list =gen_machine_code(c_line,label_map)

with open(output_file, 'w') as f:
    for b in b_output:
        f.write(b + '\n')





        












