from function_details import FunctionDetails
#
# Semantic anaĺysis and structures
#
#################
# Semantic Cube #
#################
# Operator values
# 1: +
# 2: -
# 3: *
# 4: /
# 5: %
# 6: =
# 7: ==
# 8: >
# 9: <
# 10: <=
# 11: >=
# 12: <>
# 13: &&
# 14: ||

# Cube declaration
# -1 as return value used for errors
# 0-indexed dimentions not used to avoid extra logic with type translation
semantic_cube = [[[-1 for i in range(15)] for j in range(6)] for i in range(6)]

# First index is for first operand
# Second index is for second operand
# Third index is for binary operator specified in comment above
# Only operations that doesn't return errors are defined

# Integer operations
semantic_cube[1][1][1] = 1 # int + int = int
semantic_cube[1][1][2] = 1 # int - int = int
semantic_cube[1][1][3] = 1 # int * int = int
semantic_cube[1][1][4] = 2 # int / int = float
semantic_cube[1][1][5] = 2 # int % int = float
semantic_cube[1][1][6] = 1 # int = int = int
semantic_cube[1][2][1] = 2 # int + float = float
semantic_cube[1][2][2] = 2 # int - float = float
semantic_cube[1][2][3] = 2 # int * float = float
semantic_cube[1][2][4] = 2 # int / float = float
semantic_cube[1][2][5] = 2 # int % float = float
semantic_cube[1][2][6] = 1 # int = float = int
semantic_cube[1][1][7] = 4 # int == int = bool
semantic_cube[1][1][8] = 4 # int > int = bool
semantic_cube[1][1][9] = 4 # int < int = bool
semantic_cube[1][1][10] = 4 # int <= int = bool
semantic_cube[1][1][11] = 4 # int >= int = bool
semantic_cube[1][1][12] = 4 # int <> int = bool

# Float operations
semantic_cube[2][2][1] = 2 # float + float = float
semantic_cube[2][2][2] = 2 # float - float = float
semantic_cube[2][2][3] = 2 # float * float = float
semantic_cube[2][2][4] = 2 # float / float = float
semantic_cube[2][2][5] = 2 # float % float = float
semantic_cube[2][2][6] = 2 # float = float = float
semantic_cube[2][1][1] = 2 # float + int = float
semantic_cube[2][1][2] = 2 # float - int = float
semantic_cube[2][1][3] = 2 # float * int = float
semantic_cube[2][1][4] = 2 # float / int = float
semantic_cube[2][1][5] = 2 # float % int = float
semantic_cube[2][1][6] = 2 # float = int = float
semantic_cube[2][2][7] = 4 # float == float = bool
semantic_cube[2][2][8] = 4 # float > float = bool
semantic_cube[2][2][9] = 4 # float < float = bool
semantic_cube[2][2][10] = 4 # float <= float = bool
semantic_cube[2][2][11] = 4 # float >= float = bool
semantic_cube[2][2][12] = 4 # float <> float = bool

# Boolean operations
semantic_cube[4][4][6] = 4 # bool = bool = bool
semantic_cube[4][4][7] = 4 # bool == bool = bool
semantic_cube[4][4][8] = 4 # bool > bool = bool
semantic_cube[4][4][9] = 4 # bool < bool = bool
semantic_cube[4][4][10] = 4 # bool <= bool = bool
semantic_cube[4][4][11] = 4 # bool >= bool = bool
semantic_cube[4][4][12] = 4 # bool <> bool = bool

###################
# Data structures #
###################
current_scope = 'global'
current_type = ''
current_id = ''
current_params_types = []
current_params_ids = []
current_function = {
  'id'           : '',
  'type'         : '',
  'params_types' : [],
  'params_ids'   : [],
  'mem_needed'   : []
}

# Variables dictionary with scope
variables = {
  'global' : {
  },
  'function' : {
  }
}

# Functions dictionary
functions = {}

# Constants dictionary
constants = {}

# Translation of types to int
int_types = {
  'int'     : 1,
  'float'   : 2,
  'str'     : 3,
  'bool'    : 4,
  'void'    : 5,
  'error'   : -1
}

# Translation of types to string
string_types = {v: k for k, v in int_types.items()}

operations = {
 '+'     : 1,
 '-'     : 2,
 '*'     : 3,
 '/'     : 4,
 '%'     : 5,
 '='     : 6,
 '=='    : 7,
 '>'     : 8,
 '<'     : 9,
 '<='    : 10,
 '>='    : 11,
 '<>'    : 12,
 '&&'    : 13,
 '||'    : 14,
 '('     : 15,
 ')'     : 16,
 'goto'  : 17,
 'gotof' : 18,
 'gotoz' : 19,
 'READ'  : 20,
 'WRITE' : 21,
 'RET'   : 22,
 'EP'    : 23, # End Program
 'DIM'   : 24  # Substract value of given quadruple by one (used for repeat only)
}

inverse_operations = {v: k for k, v in operations.items()}

#####################
# Memory management #
#####################

# Memory counters per data type
# int, float, string, bool
global_mem_counter    = [0, 1500, 3000, 4500]
constants_mem_counter = [6000, 7500, 9000, 10500]
function_mem_counter  = [12000, 13500, 15000, 16500]
# Temporals array might not be needed 
# temporals_mem_counter = [18000, 19500, 21000, 22500]

# Actual Memory
# Lists of list, each list consisting of data types
# Sublist 0: int, 1: float, 2: string, 3: bool
global_memory    = [[] for i in range(4)]
constants_memory = [[] for i in range(4)]
function_memory  = [[] for i in range(4)]

# Function that resets virtual memory counters
# And adds to function details memory needed
def reset_mem_counter():
  global function_mem_counter, current_function
  # Get memory needed per data type for current function
  memory_needed = [function_mem_counter[0] - 12000,
                function_mem_counter[1] - 13500,
                function_mem_counter[2] - 15000,
                function_mem_counter[3] - 16500]

  # Set memory needed per data type for current function
  functions[current_function['id']].mem_needed = memory_needed
  # print(functions[current_function['id']].mem_needed)

  # Reset function memory counters
  function_mem_counter[0] = 12000
  function_mem_counter[1] = 13500
  function_mem_counter[2] = 15000
  function_mem_counter[3] = 16500

# Given scope and data type of variable, return corresponding virtual memory index
def get_var_mem(scope, vtype):
  if(scope == 'global'): # Condition to check which counter should be accessed
    if(vtype == 'int'): # Condition to check which index should be modified
      global_mem_counter[0] += 1 # Add one to memory counter
      if(global_mem_counter[0] > 1499): # Check if too many variables
        print('Memory Exceeded.')
        exit(0) # Too many variables
      return global_mem_counter[0] - 1 # Return virtual memory position
    elif(vtype == 'float'):
      global_mem_counter[1] += 1
      if(global_mem_counter[1] > 2999):
        print('Memory Exceeded.')
        exit(0)
      return global_mem_counter[1] - 1
    elif(vtype == 'string'):
      global_mem_counter[2] += 1
      if(global_mem_counter[2] > 4499):
        print('Memory Exceeded.')
        exit(0)
      return global_mem_counter[2] - 1
    elif(vtype == 'bool'):
      global_mem_counter[3] += 1
      if(global_mem_counter[3] > 5999):
        print('Memory Exceeded.')
        exit(0)
      return global_mem_counter[3] - 1
  else: # If it's not global, then we don't care about the scope. We know it's a function
    if(vtype == 'int'): # Conditionto check which index should be modified
      function_mem_counter[0] += 1 # Add one to memory counter
      if(function_mem_counter[0] > 13499): # Check if too many variables
        print('Memory Exceeded.')
        exit(0) # Too many variables
      return function_mem_counter[0] - 1 # Return virtual memory position
    elif(vtype == 'float'):
      function_mem_counter[1] += 1
      if(function_mem_counter[1] > 14999):
        print('Memory Exceeded.')
        exit(0)
      return function_mem_counter[1] - 1
    elif(vtype == 'string'):
      function_mem_counter[2] += 1
      if(function_mem_counter[2] > 16499):
        print('Memory Exceeded.')
        exit(0)
      return function_mem_counter[2] - 1
    elif(vtype == 'bool'):
      function_mem_counter[3] += 1
      if(function_mem_counter[3] > 17999):
        print('Memory Exceeded.')
        exit(0)
      return function_mem_counter[3] - 1

def append_const(cons, cons_type):
  if(cons_type == 'int'): # Condition to check which index should be modified
    constants_mem_counter[0] += 1 # Add one to memory counter
    if(constants_mem_counter[0] > 7499): # Check if too many variables
      print('Memory Exceeded.')
      exit(0) # Too many variables
    constants_memory[0].append(cons)
    return constants_mem_counter[0] - 1 # Return virtual memory position
  elif(cons_type == 'float'):
    constants_mem_counter[1] += 1
    if(constants_mem_counter[1] > 8999):
      print('Memory Exceeded.')
      exit(0)
    constants_memory[1].append(cons)
    return constants_mem_counter[1] - 1
  elif(cons_type == 'string'):
    constants_mem_counter[2] += 1
    if(constants_mem_counter[2] > 10499):
      print('Memory Exceeded.')
      exit(0)
    constants_memory[2].append(cons)
    return constants_mem_counter[2] - 1
  elif(cons_type == 'bool'):
    constants_mem_counter[3] += 1
    if(constants_mem_counter[3] > 11999):
      print('Memory Exceeded.')
      exit(0)
    constants_memory[3].append(cons)
    return constants_mem_counter[3] - 1

def get_operand_mem(op, cf):
  current_function = cf
  var_mem = None
  if op in variables['function'][current_function['id']]:
    var_det = variables['function'][current_function['id']][op]
    var_mem = var_det.vmemory
  elif op in variables['global']:
    var_det = variables['global'][op]
    var_mem = var_det.vmemory
  else:
    print('Undefined variable ', op)
    exit(0)
  return var_mem

def memory_to_data_type(mem):
  if((mem >= 0 and mem < 1500) or 
     (mem >= 6000 and mem < 7500) or
     (mem >= 12000 and mem < 13500)):
    return 'int'
  elif((mem >= 1500 and mem < 3000) or 
       (mem >= 7500 and mem < 9000) or
       (mem >= 13500 and mem < 15000)):
    return 'float'
  elif((mem >= 3000 and mem < 4500) or 
       (mem >= 9000 and mem < 10500) or
       (mem >= 15000 and mem < 16500)):
    return 'str'
  else:
    return 'bool'

######################
# Semantic functions #
######################

####################
# Helper Functions #
####################

def typeString(s):
    return s.split("'")[1]
