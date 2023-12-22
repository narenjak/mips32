# hello and wellcome, this a project for ACA course with dr. noori in ferdowsi university.

class Mips32:
    #constructor
    def __init__(self, m_size= 128) -> None:
        self.memory = [0 for _ in range(m_size)]
        self.register = [0 for _ in range(32)]  #32bits general-purpose registers

        self.ProgramCounter = 64
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
    def add_run(self, rs, rt, rd):
        self.register[rd] = self.register[rs] + self.register[rt]
        self.ProgramCounter += 1

    def sub_run(self, rs, rt, rd):
        self.register[rd] = self.register[rs] - self.register[rt]
        self.ProgramCounter += 1

    def or_run(self, rs, rt, rd):
        self.register[rd] = self.register[rs] or self.register[rt]
        # im so happy, because python has OR function :))
        self.ProgramCounter += 1

    def and_run(self, rs, rt, rd):
        self.register[rd] = self.register[rs] and self.register[rt]
        # im so happy, because python has AND function :))
        self.ProgramCounter += 1


    def slt_run(self, rs, rt, rd):
        if self.register[rs] < self.register[rt] :
            self.register[rd] = 1
        else: 
            self.register[rd] = 0

    def ori_run(self, rs, rt, ImmediateNum):
        self.register[rt] = self.register[rs] or ImmediateNum
        # im so happy, because python has OR function :))
        self.ProgramCounter += 1


    # if MEM[PC]==BEQ rs rt immediate16
    # target = PC + 4 + sign-extend(immediate) x 4 
    # if GPR[rs]==GPR[rt] then 	PC  target
    # else 	PC  PC + 4
    def beq_run(self, rs, rt, disAdd):
        if self.register[rt] == self.register[rs]:
            self.ProgramCounter = disAdd
        else:
            self.ProgramCounter += 1
    def bne_run(self, rs, rt, disAdd):
        if self.register[rt] != self.register[rs]:
            self.ProgramCounter = disAdd
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
        else:
            None


        