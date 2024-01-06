# hello and wellcome again, this a project for ACA course with dr. noori in ferdowsi university.

import random

class Mips32:
    #constructor
    def __init__(self, m_size= 512) -> None:
        self.memory = [0 for _ in range(m_size)]
        self.register = [0 for _ in range(32)]  #32bits general-purpose registers
        self.ProgramCounter = 256
        ################################
        # Pipeline Registers
        #IF/ID:
        self.IF_ID_NPC = 0
        self.IF_ID_IR = 0
        #ID/EX:
        self.ID_EX_NPC  = 0
        self.ID_EX_A = 0
        self.ID_EX_B = 0
        self.ID_EX_RT = 0
        self.ID_EX_RD = 0
        self.ID_EX_IMM = 0
        self.ID_EX_RS = 0
        #EX/MEM:
        self.EX_MEM_BR_TGT = 0 
        self.EX_MEM_ZERO = 0
        self.EX_MEM_ALU_OUT = 0
        self.EX_MEM_B = 0
        self.EX_MEM_RD = 0
        #MEM/WB
        self.MEM_WB_LMD = 0
        self.MEM_WB_ALU_OUT = 0
        self.MEM_WB_RD = 0
        ################################
        #control signal
        #ID/EX:
        self.ID_EX_MemToReg = 0
        self.ID_EX_RegWrite = 0
        self.ID_EX_Branch = 0
        self.ID_EX_MemRead = 0
        self.ID_EX_MemWrite = 0
        self.ID_EX_RegDst = 0
        self.ID_EX_AluSrc = 0
        self.ID_EX_AluOp = 0
        #EX/MEM:
        self.EX_MEM_MemToReg = 0
        self.EX_MEM_RegWrite = 0
        self.EX_MEM_Branch = 0
        self.EX_MEM_MemRead = 0
        self.EX_MEM_MemWrite = 0
        #MEM/WB
        self.MEM_WB_MemToReg = 0
        self.MEM_WB_RegWrite = 0
        ################################
        # Forwarding Unit Signals
        self.FWD_PC_WRITE = 1
        self.FWD_IF_ID_WRITE = 1
        self.FWD_FWD_A = 0
        self.FWD_FWD_B = 0
        self.FWD_STALL = 0
        ################################
        
        
        # Forwarding+Hazard Units helper variables
        self.outFwdA = 0
        self.outFwdB = 0
        # Error Signals
        self.EINST = -1
        self.EARG = -2
        self.EFLOW = -3
        self.ERROR = [self.EINST, self.EARG, self.EFLOW]
        # Enable or disable hazard protections
        self.data_hzd = True
        self.ctrl_hzd = True


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
        self.ProgramCounter += 1
        return self.register[rs] + self.register[rt]
    def sub_run(self, rd, rs, rt):
        self.ProgramCounter += 1
        return self.register[rs] - self.register[rt]
    def or_run(self, rd, rs, rt):
        self.ProgramCounter += 1
        return self.register[rs] or self.register[rt]
    def and_run(self, rd, rs, rt):
        self.ProgramCounter += 1
        return self.register[rs] and self.register[rt]
    def slt_run(self, rd, rs, rt):
        self.ProgramCounter += 1
        if self.register[rs] < self.register[rt] :
            return 1
        else: 
            return 0
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

        
    def loadInstructions (self, setOfInstructios):
        for i, instruction in enumerate(setOfInstructios):
            self.memory[i+256] = instruction

    def loadData (self, arrayOfdata): 
        for i, data in enumerate(arrayOfdata):
            self.memory[i] = data

    ################################
    
    def IF(self):
        try:
            currentInstruction = self.memory[self.ProgramCounter]
            curInst = currentInstruction.content.split(' ')
        except IndexError:
            curInst = 0
        
        #check for stall
        if self.FWD_IF_ID_WRITE == 1 or not self.data_hzd:
            # Set IF/ID.NPC
            self.IF_ID_NPC = self.ProgramCounter + 1
            # Set IF/ID.IR
            self.IF_ID_IR = curInst

        if self.FWD_PC_WRITE == 1 or not self.data_hzd:
            # Set own PC (PC Multiplexer)
            if self.EX_MEM_ZERO == 1 and self.EX_MEM_Branch == 1:
                self.ProgramCounter = self.EX_MEM_BR_TGT
            elif self.FWD_STALL != 1:
                self.ProgramCounter += 1

    def DE(self):
        # Set Control of ID/EX (Control Unit)
        try:
            opcode = self.IF_ID_IR[0]
        except:
            print('nothing for pipline')
            opcode = 'no operation'
        
        if self.FWD_STALL == 1:
            # Stall the pipeline, adding a bubble
            self.ID_EX_RegDst= 0
            self.ID_EX_AluSrc = 0
            self.ID_EX_MemToReg = 0
            self.ID_EX_RegWrite = 0
            self.ID_EX_MemRead = 0
            self.ID_EX_MemWrite = 0
            self.ID_EX_Branch = 0
            self.ID_EX_AluOp = 0
        else:
            # J   I      R
            #----------------
            # J	  sw	 add
            #     lw	 sub
            #     addi   or 
            #     slti   and
            #     andi   slt
            #     ori	
            #     beq	
            #     bne	
            if opcode == 'lw':
                self.ID_EX_RegDst = 0 #0->rt 1->rd
                self.ID_EX_AluSrc = 1 #0->B  1->imm
                self.ID_EX_MemToReg = 1  #dont use until ex/mem
                self.ID_EX_RegWrite = 1  #dont use until mem/wb
                self.ID_EX_MemRead = 1  #dont use until ex/mem
                self.ID_EX_MemWrite = 0  #dont use until ex/mem
                self.ID_EX_Branch = 0  #dont use until ex/mem
                self.ID_EX_AluOp = 0 #we have alu op 
            elif opcode == 'sw':
                self.ID_EX_RegDst = 0 #0->rt 1->rd
                self.ID_EX_AluSrc = 1 #0->B  1->imm
                self.ID_EX_MemToReg = 0  #dont use until ex/mem
                self.ID_EX_RegWrite = 0  #dont use until mem/wb
                self.ID_EX_MemRead = 0  #dont use until ex/mem
                self.ID_EX_MemWrite = 1  #dont use until ex/mem
                self.ID_EX_Branch = 0  #dont use until ex/mem
                self.ID_EX_AluOp = 0 #we have alu op 
            elif opcode == 'beq':
                self.ID_EX_RegDst = 0 #0->rt 1->rd
                self.ID_EX_AluSrc = 0 #0->B  1->imm
                self.ID_EX_MemToReg = 0  #dont use until ex/mem
                self.ID_EX_RegWrite = 0  #dont use until mem/wb
                self.ID_EX_MemRead = 0  #dont use until ex/mem
                self.ID_EX_MemWrite = 0  #dont use until ex/mem
                self.ID_EX_Branch = 1  #dont use until ex/mem
                self.ID_EX_AluOp = 1 #we have alu op 
            elif opcode == 'addi':
                self.ID_EX_RegDst = 0 #0->rt 1->rd
                self.ID_EX_AluSrc = 1 #0->B  1->imm
                self.ID_EX_MemToReg = 0  #dont use until ex/mem
                self.ID_EX_RegWrite = 1  #dont use until mem/wb
                self.ID_EX_MemRead = 0  #dont use until ex/mem
                self.ID_EX_MemWrite = 0  #dont use until ex/mem
                self.ID_EX_Branch = 0  #dont use until ex/mem
                self.ID_EX_AluOp = 0 #we have alu op 
            else:
                self.ID_EX_RegDst = 1 #0->rt 1->rd
                self.ID_EX_AluSrc = 0 #0->B  1->imm
                self.ID_EX_MemToReg = 0  #dont use until ex/mem
                self.ID_EX_RegWrite = 1  #dont use until mem/wb
                self.ID_EX_MemRead = 0  #dont use until ex/mem
                self.ID_EX_MemWrite = 0  #dont use until ex/mem
                self.ID_EX_Branch = 0  #dont use until ex/mem
                self.ID_EX_AluOp = 2 #we have alu op 

        # Set ID/EX.NPC
        self.ID_EX_NPC = self.IF_ID_NPC
        if opcode == 'sw' or opcode == 'lw' or opcode == 'addi' or opcode == 'slti' or opcode == 'andi' or opcode =='ori' or opcode == 'beq' or opcode == 'bne':
            # Set ID/EX.A
            self.ID_EX_A = self.register[int(self.IF_ID_IR[1])]
            # Set ID/EX.B
            self.ID_EX_B = self.register[int(self.IF_ID_IR[2])]
            # Set ID/EX.RT
            self.ID_EX_RT = self.IF_ID_IR[1]
            # Set ID/EX.RD
            self.ID_EX_RD = self.IF_ID_IR[2]
            # Set ID/EX.Imm (Sign Extend)
            self.ID_EX_IMM_ = self.IF_ID_IR[3]
            # Set ID/EX.RS
            self.ID_EX_RS = self.IF_ID_IR[1]
        elif opcode == 'add' or opcode == 'sub' or opcode == 'or' or opcode == 'and' or opcode == 'slt':
            # Set ID/EX.A
            self.ID_EX_A = self.register[int(self.IF_ID_IR[2])]
            # Set ID/EX.B
            self.ID_EX_B = self.register[int(self.IF_ID_IR[3])]
            # Set ID/EX.RT
            self.ID_EX_RT = self.IF_ID_IR[3]
            # Set ID/EX.RD
            self.ID_EX_RD = self.IF_ID_IR[1]
            # Set ID/EX.Imm (Sign Extend)
            self.ID_EX_IMM_ = 0
            # Set ID/EX.RS
            self.ID_EX_RS = self.IF_ID_IR[2]
        else:
            # Set ID/EX.A
            self.ID_EX_A = 0
            # Set ID/EX.B
            self.ID_EX_B = 0
            # Set ID/EX.RT
            self.ID_EX_RT = 0
            # Set ID/EX.RD
            self.ID_EX_RD = 0
            # Set ID/EX.Imm (Sign Extend)
            self.ID_EX_IMM_ = self.IF_ID_IR[1]
            # Set ID/EX.RS
            self.ID_EX_RS = 0

    def EX(self):
        self.EX_MEM_MemToReg = self.ID_EX_MemToReg
        self.EX_MEM_RegWrite = self.ID_EX_RegWrite
        self.EX_MEM_Branch = self.ID_EX_Branch
        self.EX_MEM_MemRead = self.ID_EX_MemRead
        self.EX_MEM_MemWrite = self.ID_EX_MemWrite
        self.EX_MEM_BR_TGT = self.ID_EX_IMM #may be we have branch
        # Set internal ALU source A
        aluA = self.outFwdA
        # Set internal ALU source B (B Multiplexer)
        if self.ID_EX_AluSrc == 1:
            aluB = self.ID_EX_IMM
        else:
            aluB = self.outFwdB
        #######################################
        # Set EX/MEM.Zero (ALU)
        if aluA - aluB == 0:
            self.EX_MEM_ZERO = 1
        else:
            self.EX_MEM_ZERO = 0
        # Set EX/MEM.AluOut (ALU + ALU Control)
        inst = self.IF_ID_IR
        out = 0
        if self.ID_EX_AluOp == 0: # l-Type
            out = aluA + aluB
        #     if curInst[0] == "sw":
        #         sw_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        #     elif curInst[0] == "lw":
        #         lw_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        #     elif curInst[0] == "addi":
        #         addi_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        #     elif curInst[0] == "slti":
        #         slti_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        #     elif curInst[0] == "andi":
        #         andi_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        #     elif curInst[0] == "ori":
        #         ori_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        #     elif curInst[0] == "beq":
        #         beq_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        #     elif curInst[0] == "bne":
        #         bne_run(int(curInst[1]),int(curInst[2]), int(curInst[3]))
        elif self.ID_EX_AluOp == 1: # j
            out = aluA - aluB
            # if curInst[0] == "j":
            #     j_run(int(curInst[1]))
        
        elif self.ID_EX_AluOp  == 2: # R-Type
            if inst[0] == "add":
                out = self.add_run(int(inst[1]),int(inst[2]), int(inst[3]))
            elif inst[0] == "sub":
                out = self.sub_run(int(inst[1]),int(inst[2]), int(inst[3]))
            elif inst[0] == "or":
                out = self.or_run(int(inst[1]),int(inst[2]), int(inst[3]))
            elif inst[0] == "and":
                out = self.and_run(int(inst[1]),int(inst[2]), int(inst[3]))
            elif inst[0] == "slt":
                out = self.slt_run(int(inst[1]),int(inst[2]), int(inst[3]))
            
        self.EX_MEM_ALU_OUT = out
        
        # Set EX/MEM.B
        self.EX_MEM_B = self.outFwdB
        # Set EX/MEM.RD (RegDst Multiplexer)
        if self.ID_EX_RegDst == 1:
            self.EX_MEM_RD = self.ID_EX_RD
        else:
            self.EX_MEM_RD = self.ID_EX_RT

    def ME(self):
        # Set Control of MEM/WB based on Control of EX/MEM
        self.MEM_WB_MemToReg = self.EX_MEM_MemToReg
        self.MEM_WB_RegWrite = self.EX_MEM_RegWrite
        # Set MEM/WB.LMD (read from Data Memory)
        if self.EX_MEM_MemRead == 1:
            # The simulation memory might not be big enough
            if self.EX_MEM_ALU_OUT < 128:
                self.MEM_WB_LMD = self.memory[self.EX_MEM_ALU_OUT]
            else:
                print('***WARNING***')
                print(f'\tMemory Read at position {self.EX_MEM_ALU_OUT} not executed:')
                print(f'\t\tMemory only has {128} positions.') 
                try:
                    input('Press ENTER to continue execution or abort with CTRL-C. ')
                except KeyboardInterrupt:
                    print('Execution aborted.')
                    exit()

        # Write to Data Memory
        if self.EX_MEM_MemWrite== 1:
            # The simulation memory might not be big enough
            if self.EX_MEM_ALU_OUT < 128:
                self.memory[self.EX_MEM_ALU_OUT] = self.EX_MEM_B
            else:
                print('***WARNING***')
                print(f'\tMemory Write at position {self.EX_MEM_ALU_OUT} not executed:')
                print(f'\t\tMemory only has {128} positions.')
                
                try:
                    input('Press ENTER to continue execution or abort with CTRL-C. ')
                except KeyboardInterrupt:
                    print('Execution aborted.')
                    exit()

        # Set MEM/WB.ALUOut
        self.MEM_WB_ALU_OUT = self.EX_MEM_ALU_OUT

        # Set MEM/WB.RD
        self.MEM_WB_RD = self.EX_MEM_RD

    def WB(self):
        # Write to Registers
        if self.MEM_WB_RegWrite == 1 and self.MEM_WB_RD != 0:
            # MemToReg Multiplexer
            if self.MEM_WB_MemToReg == 1:
                self.register[self.MEM_WB_RD] = self.MEM_WB_LMD
            else:
                self.register[self.MEM_WB_RD] = self.MEM_WB_ALU_OUT

    def EX_fwd(self):
        # Forwarding Unit
        if self.MEM_WB_RegWrite == 1 and self.MEM_WB_RD != 0 and self.MEM_WB_RD == self.ID_EX_RS and (self.EX_MEM_RD != self.ID_EX_RS or self.EX_MEM_RegWrite == 0):
            self.FWD_FWD_A = 1
        elif self.EX_MEM_RegWrite == 1 and self.EX_MEM_RD != 0 and self.EX_MEM_RD == self.ID_EX_RS:
            self.FWD_FWD_A = 2
        else:
            self.FWD_FWD_A = 0

        if self.MEM_WB_RegWrite == 1 and self.MEM_WB_RD != 0 and self.MEM_WB_RD == self.ID_EX_RT and (self.EX_MEM_RD != self.ID_EX_RT or self.EX_MEM_RegWrite == 0):
            self.FWD_FWD_B = 1
        elif self.EX_MEM_RegWrite== 1 and self.EX_MEM_RD != 0 and self.EX_MEM_RD == self.ID_EX_RT:
            self.FWD_FWD_B = 2
        else:
            self.FWD_FWD_B = 0

        # FwdA Multiplexer
        if self.FWD_FWD_A == 0 or not self.data_hzd:
            self.outFwdA = self.ID_EX_A
        elif self.FWD_FWD_A == 1:
            if self.MEM_WB_MemToReg == 1:
                self.outFwdA = self.MEM_WB_LMD
            else:
                self.outFwdA = self.MEM_WB_ALU_OUT
        elif self.FWD_FWD_A == 2:
            self.outFwdA = self.EX_MEM_ALU_OUT

        # FwdB Multiplexer
        if self.FWD_FWD_B == 0 or not self.data_hzd:
            self.outFwdB = self.ID_EX_B
        elif self.FWD_FWD_B == 1:
            # MemToReg Multiplexer
            if self.MEM_WB_MemToReg == 1:
                self.outFwdB = self.MEM_WB_LMD
            else:
                self.outFwdB = self.MEM_WB_ALU_OUT
        elif self.FWD_FWD_B == 2:
            self.outFwdB = self.EX_MEM_ALU_OUT

    def ID_hzd(self):
        # Hazard Unit
        if_id_rs = self.IF_ID_IR[1]
        if_id_rt = self.IF_ID_IR[2]

        if self.ID_EX_MemRead == 1 and (self.ID_EX_RT == if_id_rs or self.ID_EX_RT == if_id_rt) and self.data_hzd:
            self.FWD_PC_WRITE = 0
            self.FWD_IF_ID_WRITE = 0
            self.FWD_STALL = 1
        elif (self.ID_EX_Branch == 1 or self.EX_MEM_Branch == 1) and self.ctrl_hzd:
            self.FWD_IF_ID_WRITE = 0
            self.FWD_STALL = 1
        else:
            self.FWD_PC_WRITE = 1
            self.FWD_IF_ID_WRITE = 1
            self.FWD_STALL = 0


def main():
    fum_processor = Mips32()

    data = list()
    
    method = int(input("enter 1 to select randomly number, or 0 to enter numbers manuly"))
    
    if method == 1: 
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
        "beq 4 6 2",    # 264 -> if r4 == r6 -> pc + 2
        "lw 1 0 0",     # 265 -> update smallest value
        "slt 4 2 3",    # 266 -> if r2<r3 -> r4 = 1 else 0
        "beq 4 6 2",    # 267 -> if r4 == r6 -> pc + 2
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


    clk = 0
    while(clk >= 0):
        if fum_processor.memory[fum_processor.ProgramCounter].split(' ')[0] == 'end':
            break
        # Run all stages 'in parallel'
        fum_processor.EX_fwd()
        fum_processor.WB()
        fum_processor.ME()
        fum_processor.EX()
        fum_processor.DE()
        fum_processor.IF()
        fum_processor.ID_hzd()
        clk+=1

    print('Program ran in {clk} clocks.')
    print("min: ")
    print(fum_processor.memory[10])
    print("max: ")
    print(fum_processor.memory[11])


if __name__ == "__main__":
    main()