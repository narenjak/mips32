# hello and wellcome again, this a project for ACA course with dr. noori in ferdowsi university.

import random

# may be we should impliment 5 function for each stage so ....
# i think, we need another class for each instruction
class instruction:
    def __init__(self) -> None:
        self.content = ""
        self.stalled = False
        self.stage = "fetch"

        
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


class Mips32:
    #constructor
    def __init__(self, m_size= 512) -> None:
        self.memory = [0 for _ in range(m_size)]
        self.register = [0 for _ in range(32)]  #32bits general-purpose registers
        self.ProgramCounter = 256

# ####################################################
    # def fetch_run():
    #     #check for stall
    # def decode_run():
    #     #check for stall
    # def execute_run():
    #     #check for stall
    # def memmory_run():
    #     #check for stall
    # def writeBack_run():
    #     #check for stall
# ####################################################

    def runProgram (self):
        currentInstruction = instruction()
        currentInstruction.content = self.memory[self.ProgramCounter]
        arrayOfInstruction = currentInstruction.content.split(' ')
        
        if arrayOfInstruction[0] == "sw":
            currentInstruction.sw_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "lw":
            currentInstruction.lw_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "addi":
            currentInstruction.addi_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "slti":
            currentInstruction.slti_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "andi":
            currentInstruction.andi_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "j":
            currentInstruction.j_run(int(arrayOfInstruction[1]))
        elif arrayOfInstruction[0] == "add":
            currentInstruction.add_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "sub":
            currentInstruction.sub_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "or":
            currentInstruction.or_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "and":
            currentInstruction.and_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "slt":
            currentInstruction.slt_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "ori":
            currentInstruction.ori_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "beq":
            currentInstruction.beq_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        elif arrayOfInstruction[0] == "bne":
            currentInstruction.bne_run(int(arrayOfInstruction[1]),int(arrayOfInstruction[2]), int(arrayOfInstruction[3]))
        

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

    print("min: ")
    print(fum_processor.memory[10])
    print("max: ")
    print(fum_processor.memory[11])


if __name__ == "__main__":
    main()