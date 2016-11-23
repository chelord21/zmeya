memoryStack = zStack()

def get_scope(memAddress):
  if(memAddress < 0 or memAddress >= 18000):
    print('Memory segment overflow')
    exit(0)
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
  global global_memory, function_memory, constants_memory
  if(get_scope(memAddress) == 0):
    if(get_sublist(memAddress) == 0): # G I
      return global_memory[0][memAddress]
    elif(get_sublist(memAddress) == 1): # G F
      return global_memory[1][memAddress-1500]
    elif(get_sublist(memAddress) == 2): # G S
      return global_memory[1][memAddress-3000]
    elif(get_sublist(memAddress) == 3): # G B
      if(global_memory[1][memAddress-4500] == 'T'):
        return True
      elif(global_memory[1][memAddress-4500] == 'F'):
        return False
      else:
        return global_memory[1][memAddress-4500]
  elif(get_scope(memAddress) == 1):
    if(get_sublist(memAddress) == 0): # C I
      return constants_memory[0][memAddress-6000]
    elif(get_sublist(memAddress) == 1): # C F
      return constants_memory[1][memAddress-7500]
    elif(get_sublist(memAddress) == 2): # C S
      return constants_memory[1][memAddress-9000]
    elif(get_sublist(memAddress) == 3): # C B
      if(constants_memory[1][memAddress-10500] == 'T'):
        return True
      elif(constants_memory[1][memAddress-10500] == 'F'):
        return False
      else:
        return constants_memory[1][memAddress-10500]
  elif(get_scope(memAddress) == 2):
    if(get_sublist(memAddress) == 0): # L I
      return function_memory[0][memAddress-12000]
    elif(get_sublist(memAddress) == 1): # L F
      return function_memory[1][memAddress-13500]
    elif(get_sublist(memAddress) == 2): # L S
      return function_memory[1][memAddress-15000]
    elif(get_sublist(memAddress) == 3): # L B
      if(function_memory[1][memAddress-16500] == 'T'):
        return True
      elif(function_memory[1][memAddress-16500] == 'F'):
        return False
      else:
        return function_memory[1][memAddress-16500]

def load_initial_memory():
  global global_memory, function_memory, constants_memory
  global_memory[0] = [None] * global_mem_counter[0]
  global_memory[1] = [None] * (global_mem_counter[1] - 1500)
  global_memory[2] = [None] * (global_mem_counter[2] - 3000)
  global_memory[3] = [None] * (global_mem_counter[3] - 4500)

  # constants_memory[0] = [None] * (constants_mem_counter[0] - 6000)
  # constants_memory[1] = [None] * (constants_mem_counter[1] - 7500)
  # constants_memory[2] = [None] * (constants_mem_counter[2] - 9000)
  # constants_memory[3] = [None] * (constants_mem_counter[3] - 10500)

  # Load main memory
  main_mem_det = functions['main']
  main_mem_needed = main_mem_det.mem_needed
  function_memory[0] = [None] * main_mem_needed[0]
  function_memory[1] = [None] * main_mem_needed[1]
  function_memory[2] = [None] * main_mem_needed[2]
  function_memory[3] = [None] * main_mem_needed[3]

  zombie_memory = [[] for i in range(4)]

# global_memory    = [[] for i in range(4)]
# constants_memory = [[] for i in range(4)]
# function_memory  = [[] for i in range(4)]
def make_magic():
  global global_memory, function_memory, constants_memory
  i = 0
  while(True):
    quad = QuadrupleList.quadruple_list[i]
    if(quad.operator == 1): # +
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 + op2
      function_memory[resultAddr[1]][resultAddr[2]] = res
      # print("+")
      i += 1
    elif(quad.operator == 2): # -
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 - op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      # print("-")
      i += 1
    elif(quad.operator == 3): # *
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 * op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      # print("*")
      i += 1
    elif(quad.operator == 4): # /
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 / op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      # print("/")
      i += 1
    elif(quad.operator == 5): # %
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 % op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      # print("%")
      i += 1
    elif(quad.operator == 6): # =
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      if(resultAddr[0] == 0): # If scope is global
        global_memory[resultAddr[1]][resultAddr[2]] = get_value(quad.left)
      elif(resultAddr[0] == 1):
        constant_memory[resultAddr[1]][resultAddr[2]] = get_value(quad.left)
      else:
        function_memory[resultAddr[1]][resultAddr[2]] = get_value(quad.left)
      # print("=")
      i += 1
    elif(quad.operator == 7): # ==
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 == op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      # print("==")
      i += 1
    elif(quad.operator == 8): # >
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 > op2
      function_memory[resultAddr[1]][resultAddr[2]] = res
      # print(">")
      i += 1
    elif(quad.operator == 9): # <
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 < op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      # print("<")
      i += 1
    elif(quad.operator == 10): # <=
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 <= op2
      function_memory[resultAddr[1]][resultAddr[2]] = res
      # print("<=")
      i += 1
    elif(quad.operator == 11): # >=
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 >= op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      # print(">=")
      i += 1
    elif(quad.operator == 12): # <>
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 != op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      # print("<>")
      i += 1
    elif(quad.operator == 13): # &&
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 and op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      # print("&&")
      i += 1
    elif(quad.operator == 14): # ||
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(quad.left)
      op2 = get_value(quad.right)
      res = op1 or op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      # print("||")
      i += 1
    # elif(quad.operator == 15): # (
      # print("(")
    # elif(quad.operator == 16): # )
      # print(")")
    elif(quad.operator == 17): # goto
      i = quad.result
      # print("goto")
    elif(quad.operator == 18): # gotof
      resultAddr = get_address(quad.left)
      if(resultAddr[0] == 0): # If scope is global
        if(global_memory[resultAddr[1]][resultAddr[2]] != True or
           global_memory[resultAddr[1]][resultAddr[2]] == 'F'):
           i = quad.result
      elif(resultAddr[0] == 1):
        if(constant_memory[resultAddr[1]][resultAddr[2]] != True or
           constant_memory[resultAddr[1]][resultAddr[2]] == 'F'):
           i = quad.result
      elif(resultAddr[0] == 2):
        if(function_memory[resultAddr[1]][resultAddr[2]] != True or
           function_memory[resultAddr[1]][resultAddr[2]] == 'F'):
           i = quad.result
      else:
        i += 1
      # print("gotof")
    elif(quad.operator == 19): # gotoz
      if(quad.left == 0):
        i = quad.result
      else:
        i += 1
      # print("gotoz")
    # elif(quad.operator == 20): # READ
      # print("READ")
    elif(quad.operator == 21): # WRITE
      print(get_value(quad.result))
      # print("WRITE")
      i += 1
    # elif(quad.operator == 22): # RET
      # print("RET")
    elif(quad.operator == 23): # EPROC
      mem = memoryStack.pop()
      function_memory = mem.memory
      i = mem.last_quadruple
      # print("EPROC")
    elif(quad.operator == 24): # EPROG
      # print('Program terminated')
      exit(0)
      # print("EPROG")
    elif(quad.operator == 25): # DIM
      QuadrupleList.quadruple_list[i].left -= 1
      i += 1
      # print("DIM")
    elif(quad.operator == 26): # PARAM
      tmpAddr = get_address(quad.left)
      zombie_memory[tmpAddr[1]][tmpAddr[2]] = getValue(quad.result)
      i += 1
      # print("PARAM")
    elif(quad.operator == 27): # gosub
      mem = Memory()
      mem.build(function_memory, i+1)
      memoryStack.push(mem)
      function_memory = zombie_memory
      reset_zombie_mem()
      i = quad.result
      # print("gosub")
    elif(quad.operator == 28): # ERA
      make_zombie_mem(quad.result)
      i += 1
      # print("Era")

def make_zombie_mem(fun_name):
  fun_det = functions[fun_name]
  mem_needed = fun_det.mem_needed
  zombie_memory[0] = [None] * (mem_needed[0] - 12000)
  zombie_memory[1] = [None] * (mem_needed[1] - 13500)
  zombie_memory[2] = [None] * (mem_needed[2] - 15000)
  zombie_memory[3] = [None] * (mem_needed[3] - 16500)

def reset_zombie_mem():
  zombie_memory = [[] for i in range(4)]

