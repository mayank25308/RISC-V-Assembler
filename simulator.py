
registers={"x0":"00000","x1":"00001","x2":"00010","x3":"00011",
           "x4":"00100","x5":"00101","x6":"00110","x7":"00111","x8":"01000",
           "x9":"01001","x10":"01010","x11":"01011","x12":"01100","x13":"01101",
           "x14":"01110","x15":"01111","x16":"10000","x17":"10001","x18":"10010","x19":
           "10011","x20":"10100","x21":"10101","x22":"10110","x23":"10111","x24":"11000","x25":"11001",
           "x26":"11010","x27":"11011","x28":"11100","x29":"11101","x30 ":"11110","x31 ":"11111"}

Rtype={"add":{"opcode":"0110011","func3":"000","func7":"0000000"},
       "sub":{"opcode":"0110011","func3":"000","func7":"0100000"},
       "sll":{"opcode":"0110011","func3":"001","func7":"0000000"},
       "slt":{"opcode":"0110011","func3":"010","func7":"0000000"},
       "sltu":{"opcode":"0110011","func3":"011","func7":"0000000"},
       "xor":{"opcode":"0110011","func3":"100","func7":"0000000"},
       "srl":{"opcode":"0110011","func3":"101","func7":"0000000"},
       "or":{"opcode":"0110011","func3":"110","func7":"0000000"},
       "and":{"opcode":"0110011","func3":"111","func7":"0000000"}}


def read_file(input):
    with open(input,'r') as file:
        info=file.readlines()
    lines=[]
    for i in info:
        i=i.strip()
        if i!="":
            lines.append(i)
    print(lines)

read_file("input.txt")
        
# this function will read the input filr and store the instructions in a list