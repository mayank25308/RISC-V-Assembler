p_mem= []
registers= [0]*32
pc= 0
stack_mem= [0]*32
data_mem= [0]*32
output_l= []
error= False
def to_int(bits):
    val=int(bits,2)

    if bits[0]=="1":
        val=val-(2**len(bits))
    return val

def signed(val):
    if val & (1<<31):
        return val - (1<<32)
    return val


def read(f_name):
    with open(f_name, "r") as f:
        for line in f:
            p_mem.append(line.strip())


    
def form():
    parts = []
    parts.append("0b" + format(pc & 0xFFFFFFFF, "032b"))
    for i in registers:
        parts.append("0b" + format(i & 0xFFFFFFFF, "032b"))
    return " ".join(parts)
    
def exe_jalr(instr):
    global pc
    imm = to_int(instr[0:12])
    rs1 = int(instr[12:17],2)
    rd = int(instr[20:25],2)
    temp = pc + 4
    trgt = (registers[rs1] + imm) & 0xFFFFFFFE
    registers[rd] = temp & 0xFFFFFFFF
    registers[0]=0
    pc=trgt & 0xFFFFFFFF
    
def exe_jal(instr):
    global pc
    imm = instr[0] + instr[12:20] + instr[11] + instr[1:11] + "0"
    imm = to_int(imm)
    rd = int(instr[20:25],2)
    registers[rd] = (pc + 4) & 0xFFFFFFFF
    registers[0]=0
    pc = (pc + imm) & 0xFFFFFFFF 
    
def exe_b(instr):
    global pc
    imm = instr[0] + instr[24] + instr[1:7] + instr[20:24] + "0"
    imm = to_int(imm)
    rs1 = int(instr[12:17],2)
    rs2 = int(instr[7:12],2)
    func3 = instr[17:20]   
    check= False
    if func3=="000" :
        check= registers[rs1]==registers[rs2]
    elif func3=="001": 
        check= registers[rs1]!=registers[rs2]
    elif func3=="100" : 
        a=signed(registers[rs1])
        b=signed(registers[rs2])
        check= a < b
    elif func3=="101" : 
        a=signed(registers[rs1])
        b=signed(registers[rs2])
        check= a >= b
    elif func3=="110" : 
        check= (registers[rs1] & 0xFFFFFFFF) < (registers[rs2] & 0xFFFFFFFF)
    elif func3=="111" : 
        check= (registers[rs1] & 0xFFFFFFFF) >= (registers[rs2] & 0xFFFFFFFF)
    if check:
        pc = (pc + imm) & 0xFFFFFFFF
    else: 
        pc += 4
    registers[0]=0    
def exe_i(instr):
    global pc
    imm = to_int(instr[0:12])
    rs1 = int(instr[12:17],2)
    rd = int(instr[20:25],2)
    func3 = instr[17:20]
    if func3=="000":
        registers[rd] = (registers[rs1] + imm) & 0xFFFFFFFF
    elif func3=="011":
        u_rs1=registers[rs1] & 0xFFFFFFFF
        u_imm=imm & 0xFFFFFFFF
        registers[rd]= 1 if u_rs1 < u_imm else 0
    registers[0]=0
    pc+=4

def exe_lw(instr):
    global pc
    imm = to_int(instr[0:12])
    rs1 = int(instr[12:17],2)
    rd = int(instr[20:25],2)
    addr = (registers[rs1] + imm) & 0xFFFFFFFF
    val = mem_read(addr)
    if error:
        return
    registers[rd] = val
    registers[0]=0
    pc+=4

def exe_sw(instr):
    global pc
    imm = instr[0:7] + instr[20:25]
    imm = to_int(imm)
    rs1 = int(instr[12:17],2)
    rs2 = int(instr[7:12],2)
    addr = (registers[rs1] + imm) & 0xFFFFFFFF
    mem_write(addr, registers[rs2] & 0xFFFFFFFF) 
    if error:
        return
    registers[0]=0
    pc+=4


def exe_auipc(instr):
    global pc
    rd = int(instr[20:25],2)
    imm = instr[0:20] + "000000000000"
    registers[rd] = (pc + to_int(imm)) & 0xFFFFFFFF
    registers[0]=0
    pc+=4

def exe_lui(instr):
    global pc
    rd = int(instr[20:25],2)
    imm = instr[0:20] + "000000000000"
    registers[rd] = to_int(imm) & 0xFFFFFFFF
    registers[0]=0
    pc+=4
    
def exe_r(instr):
    global pc

    rd=int(instr[20:25],2)
    func3=instr[17:20]
    rs1=int(instr[12:17],2)
    rs2=int(instr[7:12],2)
    func7=instr[0:7]

    if func3=="000" and func7=="0000000":
        registers[rd]= (registers[rs1] + registers[rs2]) & 0xFFFFFFFF
    
    elif func3=="000" and func7=="0100000":
        registers[rd]= (registers[rs1] - registers[rs2]) & 0xFFFFFFFF
    
    elif func3=="111" and func7=="0000000":
        registers[rd]= (registers[rs1] & registers[rs2]) & 0xFFFFFFFF
    
    elif func3=="110" and func7=="0000000":
        registers[rd]= (registers[rs1] | registers[rs2]) & 0xFFFFFFFF
    elif func3=="100" and func7=="0000000":
        registers[rd]= (registers[rs1] ^ registers[rs2])  & 0xFFFFFFFF
    
    elif func3=="001" and func7=="0000000":
        shamt=registers[rs2] & 0x1F
        registers[rd]= (registers[rs1] << shamt) & 0xFFFFFFFF
    elif func3=="101" and func7=="0000000":
        shamt=registers[rs2] & 0x1F
        registers[rd]= (registers[rs1] >> shamt) & 0xFFFFFFFF
   
    elif func3=="101" and func7=="0100000":
        shamt=registers[rs2] & 0x1F
        val=signed(registers[rs1])
        registers[rd]= (val >> shamt) & 0xFFFFFFFF
    
    elif func3=="010" and func7=="0000000":
        registers[rd]= 1 if signed(registers[rs1]) < signed(registers[rs2]) else 0
    
    elif func3=="011" and func7=="0000000":
        registers[rd]= 1 if (registers[rs1] & 0xFFFFFFFF) < (registers[rs2] & 0xFFFFFFFF) else 0
    
    
    registers[0]=0
    pc+=4

def mem_read(addr):
    global error
    
    if  addr % 4 != 0:
        print(f"ERROR: Unaligned memory access at address 0x{addr:08X} for lw")
        error= True
        return 0
    
    if 0x0000 <= addr <=0x00FF:
        if addr//4 >= len(p_mem):
            print(f"ERROR: invalid memory access at address 0x{addr:08X}")
            error= True
            return 0
        return int(p_mem[addr//4],2)
    
    elif 0x0100 <= addr <=0x017F:
        return stack_mem[(addr - 0x0100)//4]
    elif 0x00010000 <= addr <=0x0001007F:
        return data_mem[(addr-0x00010000)//4]
    else:
        print(f"ERROR: Invalid memory access at address 0x{addr:08X} ")
        error= True
        return 0

def execute(instr):
    global error
    opcode=instr[25:]

    if opcode=='0110011':
        exe_r(instr)
    elif opcode=='0010011':
        exe_i(instr)
    elif opcode=='0000011':
        exe_lw(instr)
    elif opcode=='0100011':
        exe_sw(instr)
    elif opcode=='1100011':
        exe_b(instr)
    elif opcode=='1101111':
        exe_jal(instr)
    elif opcode=='1100111':
        exe_jalr(instr)
    elif opcode=='0110111':
        exe_lui(instr)
    elif opcode=='0010111':
        exe_auipc(instr)
    else:
        print("Invalid instruction opcode:", opcode)
        error= True
        return
    

import sys

def main():
    global pc, error
    input_f=sys.argv[1]
    output_f=sys.argv[2]

    read(input_f)
    registers[2]= 0x017c
    HALT = "00000000000000000000000001100011"
    while True:
        if pc//4 >= len(p_mem):
            print(f"ERROR: PC out of bounds at address 0x{pc:08X}")
            error= True
            break

        instr=p_mem[pc//4]
        

        if instr==HALT:
            output_l.append(form())
            
            break
        execute(instr)

        output_l.append(form())
        if error:
            break

    #dumping data 
    if not error:
        for i in range(32):

            addr = 0x00010000 + i * 4
            val = data_mem[i] & 0xFFFFFFFF
            output_l.append(f"0x{addr:08X}:0b{format(val, '032b')}")

    with open(output_f, "w") as f:
            f.write("\n".join(output_l) + "\n")

if __name__=="__main__":
    main()
