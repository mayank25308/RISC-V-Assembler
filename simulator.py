
registers={"x0":"00000",
           "x1":"00001",
           "x2":"00010",
           "x3":"00011",
           "x4":"00100",
           "x5":"00101",
           "x6":"00110",
           "x7":"00111",
           "x8":"01000",
           "x9":"01001",
           "x10":"01010",
           "x11":"01011",
           "x12":"01100",
           "x13":"01101",
           "x14":"01110",
           "x15":"01111",
           "x16":"10000",
           "x17":"10001",
           "x18":"10010",
           "x19":"10011",
           "x20":"10100",
           "x21":"10101",
           "x22":"10110",
           "x23":"10111",
           "x24":"11000",
           "x25":"11001",
           "x26":"11010",
           "x27":"11011",
           "x28":"11100",
           "x29":"11101",
           "x30":"11110",
           "x31":"11111",
           "zero":"00000",
           "ra":"00001",
            "sp":"00010",
            "gp":"00011",
            "tp":"00100",
            "t0":"00101",
            "t1":"00110",
            "t2":"00111",
            "s0":"01000",
            "fb":"01000",
            "s1":"01001",
            "a0":"01010",
            "a1":"01011",
            "a2":"01100",
            "a3":"01101",
            "a4":"01110",
            "a5":"01111",
            "a6":"10000",
            "a7":"10001",
            "s2":"10010",
            "s3":"10011",
            "s4":"10100",
            "s5":"10101",
            "s6":"10110",
            "s7":"10111",
            "s8":"11000",
            "s9":"11001",
            "s10":"11010",
            "s11":"11011",
            "t3":"11100",
            "t4":"11101",
            "t5":"11110",
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



# this function will read the input filr and store the instructions in a list
def read_file(file):
    try:
        with open(file,'r') as file:
            info=file.readlines()
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
        line= line.split(':')[1]
    
    line=line.replace(',',' ')
    line=line.replace('(',' ').replace(')',' ')
    
   
    line=line.strip() #to remove extra spaces at begening
   
    line=line.split()

    return(line)





