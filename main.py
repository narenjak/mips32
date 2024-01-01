# hello and wellcome again, this a project for ACA course with dr. noori in ferdowsi university.

import random
import mips2
# may be we should impliment 5 function for each stage so ....
# i think, we need another class for each instruction
# no that s bad idea

def main():
    fum_processor = mips2()

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