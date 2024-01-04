class Mips32:
    #constructor
    def __init__(self, m_size= 512) -> None:
        self.memory = [0 for _ in range(m_size)]
        self.register = [0 for _ in range(32)]  #32bits general-purpose registers
        self.ProgramCounter = 256
        
        #utility signal
        #ID/EX:
        ID_EX_MemToReg = 0
        ID_EX_RegWrite = 0
        ID_EX_Branch = 0
        ID_EX_MemRead = 0
        ID_EX_MemWrite = 0
        ID_EX_RegDst = 0
        ID_EX_AluSrc = 0
        ID_EX_AluOp = 0
        #EX/MEM :
        EX_MEM_MemToReg = 0
        EX_MEM_RegWrite = 0
        EX_MEM_Branch = 0
        EX_MEM_MemRead = 0
        EX_MEM_MemWrite = 0
        #MEM/WB
        MEM_WB_MemToReg = 0
        MEM_WB_RegWrite = 0

        # Error Signals
        self.EINST = -1
        self.EARG = -2
        self.EFLOW = -3
        self.ERROR = [self.EINST, self.EARG, self.EFLOW]

        # Enable or disable hazard protections
        self.data_hzd = True
        self.ctrl_hzd = True

        # Forwarding+Hazard Units helper variables
        self.outFwdA = 0
        self.outFwdB = 0


        # Pipeline Registers
        self.IF_ID = {'NPC': 0, 'IR': 0}
        self.ID_EX = {'NPC': 0, 'A': 0, 'B': 0, 'RT': 0, 'RD': 0, 'IMM': 0, 'RS': 0}
        self.EX_MEM = {'BR_TGT': 0, 'ZERO': 0, 'ALU_OUT': 0, 'B': 0, 'RD': 0}
        self.MEM_WB = {'LMD': 0, 'ALU_OUT': 0, 'RD': 0}

        # Forwarding Unit Signals
        self.FWD = {'PC_WRITE': 1, 'IF_ID_WRITE': 1, 'FWD_A': 0, 'FWD_B': 0, 'STALL': 0}

    def runInstruction (self):       
        #set of instruction
        def sw_run (self, rt, index, base):
            add = self.register[base]+ index
            self.memory[add] = self.register[rt] #store
            self.ProgramCounter += 1
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
            self.ProgramCounter += 1
        def j_run(self, ImmediateNum):
            self.ProgramCounter  = ImmediateNum
        def add_run(self, rd, rs, rt):
            self.register[rd] = self.register[rs] + self.register[rt]
            self.ProgramCounter += 1
        def sub_run(self, rd, rs, rt):
            self.register[rd] = self.register[rs] - self.register[rt]
            self.ProgramCounter += 1
        def or_run(self, rd, rs, rt):
            self.register[rd] = self.register[rs] or self.register[rt]
            self.ProgramCounter += 1
        def and_run(self, rd, rs, rt):
            self.register[rd] = self.register[rs] and self.register[rt]
            self.ProgramCounter += 1
        def slt_run(self, rd, rs, rt):
            if self.register[rs] < self.register[rt] :
                self.register[rd] = 1
            else: 
                self.register[rd] = 0
            self.ProgramCounter += 1
        def ori_run(self, rt, rs, ImmediateNum):
            self.register[rt] = self.register[rs] or ImmediateNum
            self.ProgramCounter += 1
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

        #fetch an instruction:
        instruction = self.memory[self.ProgramCounter]
        curInst = instruction.split(' ')

        if curInst[0] == "sw":
            sw_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif curInst[0] == "lw":
            lw_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif curInst[0] == "addi":
            addi_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif curInst[0] == "slti":
            slti_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif curInst[0] == "andi":
           andi_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif curInst[0] == "j":
            j_run(int(curInst[1]))
        elif curInst[0] == "add":
            add_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif curInst[0] == "sub":
            sub_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif curInst[0] == "or":
            or_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif curInst[0] == "and":
            and_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif curInst[0] == "slt":
            slt_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif curInst[0] == "ori":
            ori_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif curInst[0] == "beq":
            beq_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif curInst[0] == "bne":
            bne_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        
    def loadInstructions (self, setOfInstructios):
        for i, instruction in enumerate(setOfInstructios):
            self.memory[i+256] = instruction

    def loadData (self, arrayOfdata): 
        for i, data in enumerate(arrayOfdata):
            self.memory[i] = data

    def runOurProgram(self):
        while(1):
            if self.memory[self.ProgramCounter].split(' ')[0] == 'end':
                break
            self.runInstruction()
# ####################################################
    def IF(self):
        currentInstruction = self.memory[self.ProgramCounter]
        curInst = currentInstruction.content.split(' ')

        #check for stall
        if self.FWD['IF_ID_WRITE'] == 1 or not self.data_hzd:
            # Set IF/ID.NPC
            self.IF_ID['NPC'] = self.ProgramCounter + 1
            # Set IF/ID.IR
            self.IF_ID['IR'] = curInst

        if self.FWD['PC_WRITE'] == 1 or not self.data_hzd:
            # Set own PC (PC Multiplexer)
            if self.EX_MEM['ZERO'] == 1 and self.EX_MEM_CTRL['BRANCH'] == 1:
                self.ProgramCounter = self.EX_MEM['BR_TGT']
            elif self.FWD['STALL'] != 1:
                self.ProgramCounter += 1

    def DE(self):
        
        # Set ID/EX.NPC
        self.ID_EX['NPC'] = self.IF_ID['NPC']

        # Set ID/EX.A
        reg1 = (self.IF_ID['IR'] & 0x03E00000) >> 21 # IR[25..21]
        self.ID_EX['A'] = self.REGS[reg1]

        # Set ID/EX.B
        reg2 = (self.IF_ID['IR'] & 0x001F0000) >> 16 # IR[20..16]
        self.ID_EX['B'] = self.

        # Set ID/EX.RT
        self.ID_EX['RT'] = (self.IF_ID['IR'] & 0x001F0000) >> 16 # IR[20..16]

        # Set ID/EX.RD
        self.ID_EX['RD'] = (self.IF_ID['IR'] & 0x0000F800) >> 11 # IR[15..11]

        # Set ID/EX.Imm (Sign Extend)
        imm = (self.IF_ID['IR'] & 0x0000FFFF) >> 0 # IR[15..0]
        self.ID_EX['IMM'] = imm

        # Set ID/EX.RS
        self.ID_EX['RS'] = (self.IF_ID['IR'] & 0x03E00000) >> 21 # IR[25..21]



    # def EX():
    #     #check for stall
    # def ME():
    #     #check for stall
    # def WB():
    #     #check for stall
# ####################################################

    
        