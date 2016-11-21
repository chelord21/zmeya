from parser import *

memoryStack = zStack()

def get_scope(memAddress):
    if(memAddress < 0 or memAddress >= 1800):
        return -1 #Error
    if(memAddress < 6000):
        return 0 #global
    elif(memAddress < 12000):
        return 1 #constant
    elif(memAddress < 18000):
        return 2 #local

def get_sublist(memAddress):
    memAddress = memAddress % 6000
    if(memAddress < 1500):
        return 0 #int
    elif(memAddress < 3000):
        return 1 #float
    elif(memAddress < 4500):
        return 2 #string
    elif(memAddress < 6000):
        return 3 #bool

# Returns [scope, data_type, real mem address]
def get_address(memAddress):
    if(get_scope(memAddress) == 0):
        if(get_sublist(memAddress) == 0): # G I
            return [0,0,memAddress]
        elif(get_sublist(memAddress) == 1): # G F
            return [0,1,memAddress-1500]
        elif(get_sublist(memAddress) == 2): # G S
            return [0,2,memAddress-3000]
        elif(get_sublist(memAddress) == 3): # G B
            return [0,3,memAddress-4500]
    elif(get_scope(memAddress) == 1):
        if(get_sublist(memAddress) == 0): # C I
            return [1,0,memAddress-6000]
        elif(get_sublist(memAddress) == 1): # C F
            return [1,1,memAddress-7500]
        elif(get_sublist(memAddress) == 2): # C S
            return [1,2,memAddress-9000]
        elif(get_sublist(memAddress) == 3): # C B
            return [1,3,memAddress-10500]
    elif(get_scope(memAddress) == 2):
        if(get_sublist(memAddress) == 0): # L I
            return [2,0,memAddress-12000]
        elif(get_sublist(memAddress) == 1): # L F
            return [2,1,memAddress-13500]
        elif(get_sublist(memAddress) == 2): # L S
            return [2,2,memAddress-15000]
        elif(get_sublist(memAddress) == 3): # L B
            return [2,3,memAddress-16500]

def get_value(memAddress):
    if(get_scope(memAddress) == 0):
        if(get_sublist(memAddress) == 0): # G I
            return global_memory[0][memAddress]
        elif(get_sublist(memAddress) == 1): # G F
            return global_memory[1][memAddress-1500]
        elif(get_sublist(memAddress) == 2): # G S
            return global_memory[1][memAddress-3000]
        elif(get_sublist(memAddress) == 3): # G B
            return global_memory[1][memAddress-4500]
    elif(get_scope(memAddress) == 1):
        if(get_sublist(memAddress) == 0): # C I
            return constants_memory[0][memAddress-6000]
        elif(get_sublist(memAddress) == 1): # C F
            return constants_memory[1][memAddress-7500]
        elif(get_sublist(memAddress) == 2): # C S
            return constants_memory[1][memAddress-9000]
        elif(get_sublist(memAddress) == 3): # C B
            return constants_memory[1][memAddress-10500]
    elif(get_scope(memAddress) == 2):
        if(get_sublist(memAddress) == 0): # L I
            return function_memory[0][memAddress-12000]
        elif(get_sublist(memAddress) == 1): # L F
            return function_memory[1][memAddress-13500]
        elif(get_sublist(memAddress) == 2): # L S
            return function_memory[1][memAddress-15000]
        elif(get_sublist(memAddress) == 3): # L B
            return function_memory[1][memAddress-16500]

# TODO: Load memory needed for globals, constants & local

for quad in QuadrupleList.quadruple_list:
    if quad.operator == 1: # +
        resultAddr = getAddress(quad.result)
        

        print("+")
    elif quad.operator == 2: # -
        print("-")
    elif quad.operator == 3: # *
        print("*")
    elif quad.operator == 4: # /
        print("/")
    elif quad.operator == 5: # %
        print("%")
    elif quad.operator == 6: # =
        print("=")
    elif quad.operator == 7: # ==
        print("==")
    elif quad.operator == 8: # >
        print(">")
    elif quad.operator == 9: # <
        print("<")
    elif quad.operator == 10: # <=
        print("<=")
    elif quad.operator == 11: # >=
        print(">=")
    elif quad.operator == 12: # <>
        print("<>")
    elif quad.operator == 13: # &&
        print("&&")
    elif quad.operator == 14: # ||
        print("||")
    elif quad.operator == 15: # (
        print("(")
    elif quad.operator == 16: # )
        print(")")
    elif quad.operator == 17: # goto
        print("goto")
    elif quad.operator == 18: # gotof
        print("gotof")
    elif quad.operator == 19: # gotoz
        print("gotoz")
    elif quad.operator == 20: # READ
        print("READ")
    elif quad.operator == 21: # WRITE
        print("WRITE")
    elif quad.operator == 22: # RET
        print("RET")
    elif quad.operator == 23: # EPROC
        print("EPROC")
    elif quad.operator == 24: # EPROG
        print("EPROG")
    elif quad.operator == 25: # DIM
        print("DIM")
