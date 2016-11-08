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
semantic_cube[1][1][7] = 4 # int == int = bool
semantic_cube[1][1][8] = 4 # int > int = bool
semantic_cube[1][1][9] = 4 # int < int = bool
semantic_cube[1][1][10] = 4 # int <= int = bool
semantic_cube[1][1][11] = 4 # int >= int = bool
semantic_cube[1][1][12] = 4 # int <> int = bool

# Float operations
semantic_cube[2][2][2] = 2 # float + float = float
semantic_cube[2][2][2] = 2 # float - float = float
semantic_cube[2][2][3] = 2 # float * float = float
semantic_cube[2][2][4] = 2 # float / float = float
semantic_cube[2][2][5] = 2 # float % float = float
semantic_cube[2][2][6] = 2 # float = float = float
semantic_cube[2][2][7] = 4 # float == float = bool
semantic_cube[2][2][8] = 4 # float > float = bool
semantic_cube[2][2][9] = 4 # float < float = bool
semantic_cube[2][2][10] = 4 # float <= float = bool
semantic_cube[2][2][11] = 4 # float >= float = bool
semantic_cube[2][2][12] = 4 # float <> float = bool

# Boolean operations
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
  'params_ids'   : []
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
  'string'  : 3,
  'bool'    : 4,
  'void'    : 5,
  'error'   : -1
}

# Translation of types to int
string_types = {
   1 : 'int',
   2 : 'float',
   3 : 'string',
   4 : 'bool',
   5 : 'void',
  -1 : 'error'
}

operators = {
 '+'  : 1,
 '-'  : 2,
 '*'  : 3,
 '/'  : 4,
 '%'  : 5,
 '='  : 6,
 '==' : 7,
 '>'  : 8,
 '<'  : 9,
 '<=' : 10,
 '>=' : 11,
 '<>' : 12,
 '&&' : 13,
 '||' : 14
}

######################
# Semantic functions #
######################
def add_to_fun_dict():
  global functions, current_function, current_scope
  print('Saving function ', current_function['id'])
  functions[current_function['id']] = FunctionDetails(current_function['type'],
                                                      current_function['params_types'],
                                                      current_function['params_ids'])
  current_scope = 'function'
  print('Saved in functions[', current_function['id'], ']')

def reset_current_function():
  global current_function
  current_function = {
    'id'           : '',
    'type'         : '',
    'params_types' : [],
    'params_ids'   : []
  }
