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


    
def mem_write(addr, value):
    global error

    if addr % 4 != 0:
        print(f"ERROR: Unaligned memory access at address 0x{addr:08X} for sw")
        error= True
        return
    
    if 0x0000 <= addr <=0x00FF:
        print(f"ERROR: Invalid memory access at address 0x{addr:08X} for sw")
        error= True
        return


    if 0x0100<= addr<= 0x017F:
         stack_mem[(addr - 0x0100) // 4] = value
    elif 0x00010000 <= addr <= 0x0001007F:
        data_mem[(addr - 0x00010000) // 4] = value
    else:
        print(f"ERROR: Invalid memory access at address 0x{addr:08X} ")
        error= True
        return
    
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
    
