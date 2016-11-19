# -*- coding: utf-8 -*-
# Analizador sintáctico de Zmeya
# Marcelo Salcedo A01195804
# Sergio Cordero a01191167

# Imports
from variable_details import VariableDetails
from function_details import FunctionDetails
from quadruple import *
import ply.yacc as yacc
import lexer

tokens = lexer.tokens

#Operation structures
operands = zStack()
operators = zStack()
# types = zStack()
tempQuad = Quadruple()
#arithmetic
tempCount = 1
repeatCount = 1

def p_program(t):
  'program : decl_kleen function_kleen main print_everything'
  print('PROGRAM')

def p_decl_kleen(t):
  '''decl_kleen : empty
                | declaration decl_kleen'''
  # print('DECL KLEEN')

def p_function_kleen(t):
  '''function_kleen : empty
                    | function function_kleen'''
  # print('FUNCTION KLEEN')

def p_assignment(t):
  'assignment : assignation_variable EQUALS expresion'
  assignment_quadruple()
  # print('ASSIGNMENT')

def p_assignation_variable(t):
  'assignation_variable : ID ass_opt_array'

def p_ass_opt_array(t):
  '''ass_opt_array : dimensions
                   | ass_var_to_stack'''

def p_ass_var_to_stack(t):
  '''ass_var_to_stack : '''
  operands.push(t[-1])

def p_atomic(t):
  '''atomic : STRING
            | INT
            | FLOAT
            | BOOL'''
  global current_type
  current_type = t[1]
  # print('Current type: ', current_type)
  # print('ATOMIC')

def p_block(t):
  'block : L_BRACE decl_kleen content_kleen R_BRACE'
  # print('BLOCK')

def p_condition(t):
  'condition : IF L_PAREN expresion R_PAREN if_quadruple oblock complete_if else_condition'
  # print('CONDITION')

def p_if_quadruple(t):
  '''if_quadruple : '''
  if_quadruple()

def p_complete_if(t):
  '''complete_if : '''
  complete_if()

def p_else_condition(t):
  '''else_condition : empty
                    | ELSE else_quadruple oblock else_finish_quad'''
  # print('ELSE CONDITION')

def p_else_quadruple(t):
  '''else_quadruple : '''
  else_quadruple()

def p_else_finish_quad(t):
  '''else_finish_quad : '''
  else_finish_quadruple()

def p_constant(t):
  '''constant : INT_CONST
              | FLOAT_CONST
              | TRUE
              | FALSE'''
  global constants
  cons_type = typeString(str(type(t[1]))) # Takes constant data type
  cons_type = 'bool' if t[1] == 'T' or t[1] == 'F' else cons_type # Make T and F bool type because python recognize them as string
  constants[t[1]] = cons_type # Save it in constants hash
  cons_mem = append_const(t[1], cons_type) # Get virtual memory of hash
  # operands.push(t[1]) # Push literal constant to operands stack
  operands.push(cons_mem)
  # print(operands.top())
  # types.push(type(t[1]))
  # print('CONSTANT: ' + str(t[1]))

def p_content(t):
  '''content : sentence
             | loops
             | condition'''
  # print('CONTENT')

def p_declaration(t):
  'declaration : VAR variable COLON atomic SEMICOLON'
  global current_scope, current_type, current_id, current_function
  if current_scope == 'global':
    variables[current_scope][current_id] = VariableDetails(current_type, get_var_mem(current_scope, current_type))
  else:
    aux_dict = variables[current_scope]
    aux_dict[current_function['id']][current_id] = VariableDetails(current_type, get_var_mem(current_scope, current_type))
  current_type = ''
  current_id = ''
  # print('DECLARATION')

def p_dimensions(t):
  'dimensions : L_BRACKET INT_CONST R_BRACKET dim_loop'
  # print('DIMENSIONS')

def p_dim_loop(t):
  '''dim_loop : dimensions
              | empty'''
  # print('DIM LOOP')

def p_expresion(t):
  'expresion : level3 expresion_loop'
  # print('EXPRESION: ')
  # QuadrupleList.print()

def p_expresion_loop(t):
  '''expresion_loop : expresion_operations expresion
                    | empty'''
  # print('EXPRESION LOOP')

def p_expresion_operations(t):
    '''expresion_operations : OR
                            | AND'''
    push_operator(t)

def p_void_fun_call(t):
  'void_fun_call : ID_FUN check_void_fun_call L_PAREN fun_call_opts R_PAREN fun_call_quadruples'

def p_check_void_fun_call(t):
  '''check_void_fun_call : '''
  global current_fun_call, functions
  fun_id = t[-1]
  if check_fun_call_exist(fun_id):
    fun_det = functions[fun_id]
    if fun_det.ftype == 'void':
      current_fun_call = t[-1]
    else:
      print('Error calling \'', fun_id, '\'. It should be a void function or assign the return value to a variable.')
      exit(0)
  else:
    print('Function ', t[-1], ' was not declared.')
    exit(0)


def p_fun_call(t):
  'fun_call : ID_FUN save_fun_id L_PAREN fun_call_opts R_PAREN fun_call_quadruples'
  # print('FUN CALL')

def p_save_fun_id(t):
  '''save_fun_id : '''
  global current_fun_call
  if check_fun_call_exist(t[-1]):
    current_fun_call = t[-1]
  else:
    print('Function ', t[-1], ' was not declared.')
    exit(0)

def p_fun_call_opts(t):
  '''fun_call_opts : empty
                   | expresion set_fun_call_param funcall_params_loop'''
  # print('FUN CALL OPTS')

def p_set_fun_call_param(t):
  '''set_fun_call_param : '''
  add_fun_call_param()

def p_funcall_params_loop(t):
  '''funcall_params_loop : empty
                         | COMMA fun_call_opts'''
  # print('FUNCALL PARAMS LOOP')

def p_fun_call_quadruples(t):
  '''fun_call_quadruples : '''
  fun_call_quadruples()

def p_function(t):
  'function : ID_FUN set_fun_id COLON function_types'
  tempQuad = Quadruple()
  tempQuad.build(operations['EPROC'], None, None, None)
  QuadrupleList.push(tempQuad)
  reset_mem_counter()
  reset_current_function()
  # print('FUNCTION')

def p_set_fun_id(t):
  '''set_fun_id : '''
  global current_function
  current_function['id'] = t[-1]
  # print('Current function id: ', current_function['id'])

def p_function_types(t):
  '''function_types : vfunction
                    | rfunction'''
  # print('FUNCTION TYPES')

## LEVEL 0 - constant, variable, fun_call, parenthesis
def p_level0(t):
  '''level0 : L_PAREN add_bottom expresion R_PAREN remove_bottom
            | constant
            | variable
            | fun_call'''
  # print('LEVEL0')

def p_add_bottom(t):
    'add_bottom : '
    #operators.push(quadruple_operations.index('('))
    operators.push(operations['('])

def p_remove_bottom(t):
    'remove_bottom : '
    operators.pop()

def p_evaluate_level0(t):
    'evaluate_level0 : '
    if(operators.size() and levels[operators.top()] == 1):
        #TODO semantic validation
        arithmetic_quadruple()

## LEVEL 1 - %, *, /
def p_level1(t):
  'level1 : level0 evaluate_level0 level1_loop'
  # print('LEVEL1')

def p_level1_loop(t):
  '''level1_loop : empty
                 | level1_opers level1'''
  # print('LEVEL1 LOOP')

def p_level1_opers(t):
    '''level1_opers : MOD
                    | DIV
                    | MULT'''
    push_operator(t)

def p_evaluate_level1(t):
    'evaluate_level1 : '
    # operators.print()
    if(operators.size() and levels[operators.top()] == 2):
        #TODO semantic validation
        arithmetic_quadruple()

## LEVEL 2 - +, -
def p_level2(t):
  'level2 : level1 evaluate_level1 level2_loop'
  # print('LEVEL2')

def p_level2_loop(t):
  '''level2_loop : level2_opers level2
                 | empty'''
  # print('LEVEL2 LOOP')

def p_level2_opers(t):
    '''level2_opers : SUM
                    | MINUS'''
    push_operator(t)

def p_evaluate_level2(t):
    'evaluate_level2 : '
    # operators.print()
    if(operators.size() and levels[operators.top()] == 3):
        #TODO semantic validation
        arithmetic_quadruple()

## LEVEL 3 - <, >, <=, >=, <>, ==
def p_level3(t):
  'level3 : level2 evaluate_level2 level3_loop'
  # print('LEVEL3')

def p_level3_loop(t):
  '''level3_loop : empty
                 | level3_opers level3'''
  # print('LEVEL3 LOOP')

def p_level3_opers(t):
  '''level3_opers : L_EQUAL
                  | G_EQUAL
                  | LESS
                  | GREATER
                  | N_EQUAL
                  | EQUALITY'''
  push_operator(t)

def p_loops(t):
  '''loops : while
           | repeat'''
  # print('LOOPS')

def p_main(t):
  'main : MAIN set_main_function block'
  tempQuad = Quadruple()
  tempQuad.build(operations['EPROG'], None, None, None)
  QuadrupleList.push(tempQuad)
  # print('MAIN')

def p_set_main_function(t):
  '''set_main_function : '''
  global current_function, variables, current_scope
  current_function['id'] = 'main'
  current_function['type'] = 'void'
  current_function['params_types'] = []
  current_function['params_ids'] = []
  variables['function']['main'] = {}
  current_scope = 'function'

def p_oblock(t):
  'oblock : L_BRACE content_kleen oblock_opt R_BRACE'
  # print('OBLOCK')

def p_oblock_opt(t):
    '''oblock_opt : RETURN expresion make_return_quad SEMICOLON
                  | empty'''
    # print('OBLOCK_OPT')

def p_make_return_quad(t):
  '''make_return_quad : '''
  return_quadruple()

def p_parameters(t):
  '''parameters : atomic set_param_type variable set_param_name params_loop'''
  # print('PARAMETERS')

# Append parameter type to the function's parameter types list
def p_set_param_type(t):
  '''set_param_type : '''
  global current_type, current_function
  current_function['params_types'].append(current_type)
  # print('Appended', current_type, 'to current_function[params_types]')
  current_type = ''
  # print('Current type after append: ', current_type)


# Append parameter id to the function's parameter names list
def p_set_param_name(t):
  '''set_param_name : '''
  global current_id, current_function
  current_function['params_ids'].append(current_id)
  # print('Appended', current_id, 'to current_function[params_ids]')
  current_id = ''
  # print('Current id after append: ', current_id)

def p_params_loop(t):
  '''params_loop : COMMA parameters
                 | empty'''
  # print('PARAMS LOOP')

def p_rblock(t):
  'rblock : L_BRACE decl_kleen content_kleen RETURN expresion make_return_quad SEMICOLON R_BRACE'
  # print('RBLOCK')

def p_content_kleen(t):
  '''content_kleen : empty
                   | content content_kleen'''
  # print('CONTENT KLEEN')

def p_read(t):
  'read : READ L_PAREN variable R_PAREN'
  # print('READ')

def p_repeat(t):
  'repeat : REPEAT L_PAREN INT_CONST get_repeat_iterations R_PAREN block finish_repeat'
  # print('REPEAT')

def p_get_repeat_iterations(t):
  '''get_repeat_iterations : '''
  repeat_quadruple(t[-1])

def p_finish_repeat(t):
  '''finish_repeat : '''
  complete_repeat()

def p_rfunction(t):
  'rfunction : atomic set_fun_type L_PAREN opt_params R_PAREN rblock'
  # print('RFUNCTION')

def p_set_fun_type(t):
  '''set_fun_type : '''
  global current_function, current_type
  current_function['type'] = current_type
  # print('Current function type: ', current_function['type'])
  current_type = ''

# Add function with its details to function dictionary and change current scope
def p_opt_params(t):
  '''opt_params : empty
                | parameters'''
  global current_scope, current_function, variables
  add_to_fun_dict()
  current_scope = 'function'
  p_ids = current_function['params_ids']
  p_types = current_function['params_types']
  for i, _aux in enumerate(p_ids):
    variables['function'][current_function['id']][p_ids[i]] = VariableDetails(p_types[i], get_var_mem('function', p_types[i]))
  # print('New scope: ', current_scope)
  # print('OPT PARAMS')

def p_sentence(t):
  '''sentence : assignment SEMICOLON
              | write SEMICOLON
              | read SEMICOLON
              | void_fun_call SEMICOLON'''
  # print('SENTENCE')

def p_variable(t):
  'variable : ID opt_array'
  global current_id, variables
  current_id = t[1] # Set variable id as current_id 
  operands.push(t[1]) # Push literal variable id to operands stack
  # types.push(type(t[1])) # Push variable type to types stack
  # print('VARIABLE')

def p_opt_array(t):
  '''opt_array : empty
               | dimensions'''
  # print('OPT ARRAY')

def p_vfunction(t):
  'vfunction : VOID set_fun_void L_PAREN opt_params R_PAREN block'
  # print('VFUNCTION')

def p_set_fun_void(t):
  '''set_fun_void : '''
  global current_function
  current_function['type'] = 'void'
  # print('Current function type: ', current_function['type'])

def p_while(t):
  'while : WHILE L_PAREN expresion while_quadruple R_PAREN block complete_while_quadruple'
  # print('WHILE')

def p_while_quadruple(t):
  '''while_quadruple : '''
  while_quadruple()

def p_complete_while_quadruple(t):
  '''complete_while_quadruple : '''
  complete_while_quadruple()

def p_write(t):
    #TODO writes with parenthesis in the expression don't work
  'write : WRITE L_PAREN write_opt R_PAREN'
  # print('WRITE')

def p_write_opt(t):
  '''write_opt : expresion write_expression
               | STRING_CONST add_string_const'''
  # print('WRITE OPT')

def p_write_expression(t):
    'write_expression : '
    #print(t[-1], "::::::")
    write_expression_quadruple(t)
    # QuadrupleList.print()
    # print('WRITE EXPRESSION')

def p_add_string_const(t):
  '''add_string_const : '''
  global constants
  constants[t[-1]] = 'string'

# Function used to print variables saved
def p_print_everything(t):
  '''print_everything : '''
  global variables, functions, constants, constants_memory
  print('Variables')
  for x in variables:
    print (x)
    for y in variables[x]:
      print (y,':',variables[x][y])
  print('Functions')
  for x in functions:
    print (x)
  print('Constants')
  for x in constants:
    print (x)
  print('--------------------')
  print('----CONSTANTS-------')
  for lists in constants_memory:
    print('Sublist[', lists, ']')
    print()
  print('--------------------')
  print('----QUADRUPLES-----')
  QuadrupleList.print()

def p_empty(p):
  'empty :'
  pass

# Check if symbol is of a certain level
levels = {1:2, # +
            2:2, # -
            3:1, # *
            4:1, # /
            5:1, # %
            6:10, # =
            7:3, # ==
            8:3, # >
            9:3, # <
            10:3, # <=
            11:3, # >=
            12:3, # <>
            13:4, # &&
            14:4, # ||
            15:0, # (
            16:0  # )
            }

# Función de error del parser
def p_error(p):
    if type(p).__name__ == 'NoneType':
      print('Syntax error')
      exit(0)
    else:
      print('Syntax error in ', p.value, ' at line ', p.lineno)
      p.lineno = 0
      exit(0)

####################
# Helper functions #
####################

def get_type_from_stack():
    return str(types.pop()).split("'")[1]

def push_operator(t):
    operators.push(operations[t[1]])

# Function that resets current_function details
def reset_current_function():
  global current_function
  current_function = {
    'id'           : '',
    'type'         : '',
    'params_types' : [],
    'params_ids'   : [],
    'mem_needed'   : []
  }

# Adds function details to function dictionary and adds 
# function index to variables['function'] dictionary
def add_to_fun_dict():
  global functions, current_function, current_scope, variables
  # print('Saving function ', current_function['id'])
  # Adds 
  functions[current_function['id']] = FunctionDetails(current_function['type'],
                                                      current_function['params_types'],
                                                      current_function['params_ids'],
                                                      current_function['mem_needed'],
                                                      QuadrupleList.next_quadruple)
  # print('Saved in functions[', current_function['id'], ']')
  # print('Current scope: ', current_scope)
  variables['function'][current_function['id']] = {}

##################################
# Quadruple generation functions #
##################################

def write_expression_quadruple(t):
    tempQuad = Quadruple()
    # TODO semantic validation between current_type and input
    lastQuad = QuadrupleList.get_last()
    operand = operands.pop()
    operation = operations['WRITE']
    tempQuad.build(operation, None, None, operand)
    QuadrupleList.push(tempQuad)

def read_quadruple():
    tempQuad = Quadruple()
    # TODO semantic validation between current_type and input
    operation = operations['READ']
    tempQuad.build(operation, None, None, current_id)
    QuadrupleList.push(tempQuad)

def assignment_quadruple():
    global variables, current_function, variables, semantic_cube
    tempQuad = Quadruple()
    operation = operations['=']
    operand = operands.pop()
    ass_variable = operands.pop()

    # Semantic evaluation
    if(ass_variable not in variables['function'][current_function['id']]):
      if(ass_variable not in variables['global']):
        print('Undefined variable ', ass_variable)
        exit(0)
      else:
        op_type = memory_to_data_type(operand)
        var_det = variables['global'][ass_variable]
        var_type = var_det.vtype
        if(semantic_cube[int_types[op_type]][int_types[var_type]][operation] == -1):
          print('Op type: ', op_type, ', Var type: ', var_type)
          print('Type mismatch in assignment to ', ass_variable)
          exit(0)
        tempQuad.build(operation, operand, None, variables['global'][ass_variable].vmemory)
        QuadrupleList.push(tempQuad)
    else:
      op_type = memory_to_data_type(operand)
      var_det = variables['function'][current_function['id']][ass_variable]
      var_type = var_det.vtype
      if(semantic_cube[int_types[op_type]][int_types[var_type]][operation] == -1):
        print('Op type: ', op_type, ', Var type: ', var_type)
        print('Type mismatch in assignment to ', ass_variable)
        exit(0)
      tempQuad.build(operation, operand, None, variables['function'][current_function['id']][ass_variable].vmemory)
      QuadrupleList.push(tempQuad)

def arithmetic_quadruple():
    global tempCount, semantic_cube, variables, current_function
    tempQuad = Quadruple()

    operator = operators.pop() # Get operator
    operand2 = operands.pop() # Get operands
    operand1 = operands.pop()

    if(typeString(str(type(operand1))) == 'str'): # Check if operand1 is a variable
      operand1 = get_operand_mem(operand1, current_function) # Gets memory for the variable
    if(typeString(str(type(operand2))) == 'str'):
      operand2 = get_operand_mem(operand2, current_function)

    type1 = memory_to_data_type(operand1) # Get type of variable/constant given the memory slot
    type2 = memory_to_data_type(operand2)

    # Semantic evaluation
    if(semantic_cube[int_types[type1]][int_types[type2]][operator] == -1):
      print('Type mismatch between ', type1, ' and ', type2)
      exit(0)

    newid = 'tmp' + str(tempCount) # Create new tmp
    tempCount += 1 # Increment tmp counter
    newid_type = string_types[semantic_cube[int_types[type1]][int_types[type2]][operator]] # Get data type of temporal
    tmp_mem = get_var_mem(current_scope, newid_type) # Assign memory to tmp
    aux_dict = variables[current_scope] # Line used to reduce next's line length
    aux_dict[current_function['id']][newid] = VariableDetails(newid_type, tmp_mem) # Saves tmp in variables hash under current_function 

    tempQuad.build(operator, operand1, operand2, tmp_mem)
    QuadrupleList.push(tempQuad)
    operands.push(tmp_mem)

# Generates while quaruple with jump pending
def while_quadruple():
  lastQuad = QuadrupleList.quadruple_list[-1] # Get last quadruple from list
  result = lastQuad.result # Get result from last quadruple
  jumps = QuadrupleList.jump_stack # Get QuadrupleList jumps stack
  jumps.push(QuadrupleList.next_quadruple) # Push into the stack next quadruple
  tempQuad = Quadruple() # Build empty quadruple
  tempQuad.build(operations['gotof'], result, None, None) # Give data to empty quadruple
  QuadrupleList.push(tempQuad) # Push quadruple to quadruples list
  # Debug
  # print('---------WHILE CHECK---------')
  # QuadrupleList.print()

# Put the corresponding jump to while quadruple previously generated
def complete_while_quadruple():
  tempQuad = Quadruple() # Build empty quadruple
  tempQuad.build(operations['goto'], None, None, QuadrupleList.jump_stack.top()) # Set jump to check while condition again
  QuadrupleList.push(tempQuad) # Push quadruple to quadruples list
  index = QuadrupleList.jump_stack.pop() # Get while quadruple index
  whileQuad = QuadrupleList.quadruple_list[index] # Get while quadruple
  whileQuad.result = QuadrupleList.next_quadruple # Set while gotof jump to next quadruple
  operands.pop()
  # Debug
  # print('---------WHILE COMPLETION CHECK---------')
  # QuadrupleList.print()

# Generates quadruple for repeat loop
def repeat_quadruple(iterations):
  # Semantic evaluation
  if(typeString(str(type(iterations))) != 'int'):
    print('Repeat loop only accepts integer numbers as parameter.')
    exit(0)
  
  jumps = QuadrupleList.jump_stack # Get QuadrupleList jumps stack
  jumps.push(QuadrupleList.next_quadruple) # Push into the stack next quadruple
  tempQuad = Quadruple()
  tempQuad.build(operations['gotoz'], iterations, None, None) # Build quadruple with new varible created as 'condition'
  QuadrupleList.push(tempQuad)

# Completes repeat gotoz quadruple and generates goto to check integer 'condition' again
def complete_repeat():  
  index = QuadrupleList.jump_stack.pop() # Get the index of repeat quadruple
  dimQuad = Quadruple()
  dimQuad.build(operations['DIM'], None, None, index) # DIM generated to substract one from gotof quadruple generated at beginning of repeat
  QuadrupleList.push(dimQuad)
  tempQuad = Quadruple()
  tempQuad.build(operations['goto'], None, None, index)
  QuadrupleList.push(tempQuad)
  repeatQuad = QuadrupleList.quadruple_list[index] # Get repeat quadruple from  list
  repeatQuad.result = QuadrupleList.next_quadruple # Set repeat gotoz jump to next quadruple

# Generates gotof quadruple after if condition token is presented
# jump pending until end of block or else encountered
def if_quadruple():
  # global operations
  jumps = QuadrupleList.jump_stack # Get jump stack from QuadrupleList class
  jumps.push(QuadrupleList.next_quadruple) # Push next_quadruple to jumps stack to keep track
  lastQuad = QuadrupleList.quadruple_list[-1] # Get last quadruple
  lastResult = lastQuad.result # Get result of expression to be evaluated in condition
  tempQuad = Quadruple()
  tempQuad.build(operations['gotof'], lastResult, None, None) # Generate gotof quadruple
  QuadrupleList.push(tempQuad) # Push it to Quadruples list
  operands.pop()
  # Debug
  # print('-----IF GENERATION CHECK-----')
  # QuadrupleList.print()

# Else encountered. Complete corresponding if quadruple and generate goto quadruple
def else_quadruple():
  # complete_if()
  jumps = QuadrupleList.jump_stack # Get jump stack from QuadrupleList class
  jumps.push(QuadrupleList.next_quadruple) # Push next_quadruple to jumps stack to keep track
  tempQuad = Quadruple()
  tempQuad.build(operations['goto'], None, None, None) # Generate goto quadruple
  QuadrupleList.push(tempQuad) # Push it to quadruples list
  # Debug
  # print('-----ELSE CHECK-----')
  # QuadrupleList.print()

# Completes corresponding if quadruple because block ended
def complete_if():
  quadIndex = QuadrupleList.jump_stack.pop() # Get the index of corresponding if quadruple to complete
  ifQuad = QuadrupleList.quadruple_list[quadIndex] # Get the quadruple
  ifQuad.result = QuadrupleList.next_quadruple + 1 # Asign next quadruple to quadruple's result
  # Debug
  # print('-----IF COMPLETION CHECK-----')
  # QuadrupleList.print()

def else_finish_quadruple():
  quadIndex = QuadrupleList.jump_stack.pop() # Get the index of corresponding if quadruple to complete
  elseQuad = QuadrupleList.quadruple_list[quadIndex] # Get the quadruple
  elseQuad.result = QuadrupleList.next_quadruple # Asign next quadruple to quadruple's result
  # Debug
  # print('-----ELSE COMPLETION CHECK-----')
  # QuadrupleList.print()

def return_quadruple():
  global current_function, variables
  return_val = operands.pop() # Gets value to be returned
  if(typeString(str(type(return_val))) == 'str'): # Check if value is a variable
    return_val = get_operand_mem(return_val, current_function) # Gets memory for the variable
  val_type = memory_to_data_type(return_val)

  # Semantic evaluation
  if(current_function['type'] != val_type):
    print('Function ', current_function['id'], ' expecting return value type \'', current_function['type'], '\', but got \'', val_type, '\'')
    exit(0)

  # TODO: INSERT FUCKING PARCHE GUADALUPANO
  # Create global variable
  global_var_type = current_function['type']
  global_var_mem = get_var_mem('global', global_var_type)
  trickQuad = Quadruple()
  trickQuad.build(operations['='], return_val, None, global_var_mem)
  QuadrupleList.push(trickQuad)
  variables['global'][current_function['id']] = VariableDetails(global_var_type, global_var_mem)
  operands.push(current_function['id'])

  tempQuad = Quadruple()
  tempQuad.build(operations['RET'], None, None, global_var_mem)
  QuadrupleList.push(tempQuad)

def add_fun_call_param():
  global fun_call_params
  value = operands.pop() # Get result from expression
  fun_call_params.append(value)

def fun_call_quadruples():
  global fun_call_params, functions, current_fun_call, variables
  types_list = []
  for val in fun_call_params:
    types_list.append(typeString(str(type(val)))) # Append into type's list the type of the value sent as param
  
  fun_details = functions[current_fun_call] # Get function details
  # Semantic evaluation
  if(types_list != fun_details.params_types):
    print('Function call to ', current_fun_call, ' doesn\'t match declaration in paramters')
    exit(0)

  fun_first_quad = fun_details.initial_quad # Get first quadruple of the function
  tmpQuad = Quadruple()
  tmpQuad.build(operations['ERA'], None, None, current_fun_call)
  QuadrupleList.push(tmpQuad) # Push to quadruples name of the function for easy search in execution time

  var_mem = None # Variables to be changed with every iteration of next loop
  var_det = None 
  # Make all the params quadruples
  for i, param in enumerate(fun_call_params):
    tmpQuad2 = Quadruple()
    var_det = variables['function'][current_fun_call][fun_details.params_names[i]]
    var_mem = var_det.vmemory
    tmpQuad2.build(operations['PARAM'], var_mem, None, fun_call_params[i])
    QuadrupleList.push(tmpQuad2)
  
  tmpQuad3 = Quadruple()
  tmpQuad3.build(operations['gosub'], None, None, fun_first_quad) # Go to subroutine's first quadruple
  QuadrupleList.push(tmpQuad3)
  
  # Reset all memory used to generate quadruples
  current_fun_call = ''
  fun_call_params = []

def check_fun_call_exist(id_fun):
  global functions
  return id_fun in functions

parser = yacc.yacc()
file = open("inputs/input.txt", "r")
yacc.parse(file.read())
file.close()
