# hello and wellcome, this a project for ACA course with dr. noori in ferdowsi university.

import random

class Mips32:
    #constructor
    def __init__(self, m_size= 512) -> None:
        self.memory = [0 for _ in range(m_size)]
        self.register = [0 for _ in range(32)]  #32bits general-purpose registers

        self.ProgramCounter = 256
        self.currentInstruction = ""

    #see Picture1.png
        
    #this instruction should be support:
       # L-Type	J-Type	R-Type
       # sw     	j	 add
       # lw		         sub
       # addi		     or 
       # slti		     and
       # andi		     slt
       #                 ori		
       #                 beq		
       #                 bne
        
    #store word:
        # if MEM[PC]==LW rt offset16 (base) 
        # EA = sign-extend(offset) + GPR[base]
        # MEM[ translate(EA) ] = GPR[rt] 
        # PC = PC + 4
    def sw_run (self, rt, index, base):
        add = self.register[base]+ index
        self.memory[add] = self.register[rt] #store
        self.ProgramCounter += 1

    #load word:
        # if MEM[PC]==LW rt offset16 (base) 
        # EA = sign-extend(offset) + GPR[base]
        # GPR[rt]  MEM[ translate(EA) ] 
        # PC  PC + 4
    def lw_run (self, rt, index, base):
        add = self.register[base]+ index
        self.register[rt] = self.memory[add] #load
        self.ProgramCounter += 1

    def addi_run (self, rt, rs, ImmediateNum):
        self.register[rt] = self.register[rs] + ImmediateNum
        self.ProgramCounter += 1

    def slti_run (self, rt, rs, ImmediateNum):
        if self.register[rs] < ImmediateNum:
            self.register[rt] = 1
        else:
            self.register[rt] = 0
        self.ProgramCounter += 1

    def andi_run (self, rt, rs, ImmediateNum):
        self.register[rt] = self.register[rs] and ImmediateNum 
        # im so happy, because python has AND function :))
        # if you dont, you can use shift
        self.ProgramCounter += 1

    #this instruction should be support:
       # L-Type	J-Type	R-Type
       # sw     	j	 add
       # lw		         sub
       # addi		     or 
       # slti		     and
       # andi		     slt
       #                 ori		
       #                 beq		
       #                 bne
    # for jump
    def j_run(self, ImmediateNum):
        self.ProgramCounter  = ImmediateNum
    
    # for R types:

    #ADD:    
    # if MEM[PC] == ADD rd rs rt
    # 	GPR[rd]  GPR[rs] + GPR[rt] 	
    # 	PC  PC + 4
    def add_run(self, rd, rs, rt):
        self.register[rd] = self.register[rs] + self.register[rt]
        self.ProgramCounter += 1

    def sub_run(self, rd, rs, rt):
        self.register[rd] = self.register[rs] - self.register[rt]
        self.ProgramCounter += 1

    def or_run(self, rd, rs, rt):
        self.register[rd] = self.register[rs] or self.register[rt]
        # im so happy, because python has OR function :))
        self.ProgramCounter += 1

    def and_run(self, rd, rs, rt):
        self.register[rd] = self.register[rs] and self.register[rt]
        # im so happy, because python has AND function :))
        self.ProgramCounter += 1


    def slt_run(self, rd, rs, rt):
        if self.register[rs] < self.register[rt] :
            self.register[rd] = 1
        else: 
            self.register[rd] = 0
        self.ProgramCounter += 1

    def ori_run(self, rt, rs, ImmediateNum):
        self.register[rt] = self.register[rs] or ImmediateNum
        # im so happy, because python has OR function :))
        self.ProgramCounter += 1


    # if MEM[PC]==BEQ rs rt immediate16
    # target = PC + 4 + sign-extend(immediate) x 4 
    # if GPR[rs]==GPR[rt] then 	PC  target
    # else 	PC  PC + 4
    def beq_run(self, rs, rt, disAdd):
        if self.register[rt] == self.register[rs]:
            self.ProgramCounter += disAdd
        else:
            self.ProgramCounter += 1
    def bne_run(self, rs, rt, disAdd):
        if self.register[rt] != self.register[rs]:
            self.ProgramCounter += disAdd
        else:
            self.ProgramCounter += 1
    

    #now we should get instructions and run them
    def runProgram (self):
        self.currentInstruction = self.memory[self.ProgramCounter]
        arrayOfInstruction = self.currentInstruction.split(' ')
        #example: we use this format-> add rd rs rt
        
        #which function should be run?
        #and call to run
        if arrayOfInstruction[0] == "sw":
            self.sw_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "lw":
            self.lw_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "addi":
            self.addi_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "slti":
            self.slti_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "andi":
            self.andi_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "j":
            self.j_run(int(arrayOfInstruction[1]))
        elif arrayOfInstruction[0] == "add":
            self.add_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "sub":
            self.sub_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "or":
            self.or_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "and":
            self.and_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "slt":
            self.slt_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "ori":
            self.ori_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "beq":
            self.beq_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "bne":
            self.bne_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        


    def loadInstructions (self, setOfInstructios):
        for i, instruction in enumerate(setOfInstructios):
            self.memory[i+256] = instruction

    def loadData (self, arrayOfdata): #because we should find max number in an array
        for i, data in enumerate(arrayOfdata):
            self.memory[i] = data

    def runOurProgram(self):
        while(1):
            if self.memory[self.ProgramCounter].split(' ')[0] == 'end':
                break
            self.runProgram()
        

def main():
    fum_processor = Mips32()

    data = list()
    
    data_method = int(input("Do you want to choose data randomly or not: (enter 1 to select randomly, enter any key or countinue)"))
    
    if data_method == 1: 
        data = [random.randint(1, 100) for _ in range(10)]
    else:
        for i in range(10):
            data.append(int(input(f"Please enter value {i + 1}: ")))
    fum_processor.loadData(data)

    print ("data added successfully")
    print (fum_processor.memory)

    program = [
        "andi 0 0 0",   # 256 -> counter as 0
        "lw 1 0 0",     # 257 -> load first element as smallest
        "lw 2 0 0",     # 258 -> load first element as largest
        "addi 0 0 1",   # 259 -> counter + 1 to change address to 1
        "andi 5 5 0",   # 260 -> make register 5 to zero
        "addi 5 5 10",  # 261 -> add 9 to register 5
        "lw 3 0 0",     # 262 -> load element based on counter address
        "slt 4 3 1",    # 263 -> if r3<r1 -> r4 = 1 else 0
        "beq 4 6 2",    # 264 -> if r4 == r5 -> pc + 2
        "lw 1 0 0",     # 265 -> update smallest value
        "slt 4 2 3",    # 266 -> if r2<r3 -> r4 = 1 else 0
        "beq 4 6 2",    # 267 -> if r4 == r5 -> pc + 2
        "lw 2 0 0",     # 268 -> update largest value
        "addi 0 0 1",   # 269 -> counter + 1
        "bne 0 5 -8",   # 270 -> if counter !== 9 countinue loop
        "sw 1 0 5",     # 271 -> store largest value to memory
        "sw 2 1 5",     # 272 -> store smallest value to memory
        "end"           # 273 -> terminate
    ]
    
    fum_processor.loadInstructions(program)
    print ("program added successfully")
    print (fum_processor.memory)

    fum_processor.runOurProgram()


    print("------------------")
    print("min: ")
    print(fum_processor.memory[10])
    print("max: ")
    print(fum_processor.memory[11])


if __name__ == "__main__":
    main()
    

