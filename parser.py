# -*- coding: utf-8 -*-
# Analizador sintáctico de Zmeya
# Marcelo Salcedo A01195804
# Sergio Cordero a01191167

# Imports
from variable_details import *
from function_details import FunctionDetails
from quadruple import *
from memory import *
# from vm import *
import ply.yacc as yacc
import lexer

tokens = lexer.tokens

#Array structures
idstack = zStack()
checkstack = zStack()
checked_dimension = 0
var = None
totalSize = 0
isArray = {}
dim = 0
r = 1
arrayDetails = ArrayDetails()
dimensionStack = zStack()
zombie_memory = [[] for i in range(4)]
#Operation structures
operands = zStack()
operators = zStack()
# types = zStack()
tempQuad = Quadruple()
#arithmetic
tempCount = 1
repeatCount = 1

def p_program(t):
  'program : goto_main decl_kleen function_kleen main print_everything'
  # print('PROGRAM')
  load_initial_memory()
  make_magic()

def p_goto_main(t):
  '''goto_main : '''
  tmpQuad = Quadruple()
  tmpQuad.build(operations['goto'], None, None, None)
  jumps = QuadrupleList.jump_stack
  jumps.push(QuadrupleList.next_quadruple)
  QuadrupleList.push(tmpQuad)

def p_decl_kleen(t):
  '''decl_kleen : empty
                | declaration decl_kleen'''
  # print('DECL KLEEN')

def p_function_kleen(t):
  '''function_kleen : empty
                    | function function_kleen'''
  # print('FUNCTION KLEEN')

def p_assignment(t):
  'assignment : variable EQUALS expresion'
  #'assignment : assignation_variable EQUALS expresion'
  assignment_quadruple()
  #print('ASSIGNMENT')

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
  'condition : IF L_PAREN add_bottom expresion R_PAREN remove_bottom if_quadruple oblock complete_if else_condition'
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
  'declaration : VAR variable_decl COLON atomic register_dimensions SEMICOLON'
  global current_scope, current_type, current_id, current_function, arrayDetails, r, totalSize, idstack, checkstack
  if current_scope == 'global':
    alfa = VariableDetails(current_type, get_var_mem(current_scope, current_type, totalSize), arrayDetails)
    #variables[current_scope][current_id] = alfa
    variables[current_scope][idstack.top()] = alfa
  else:
    aux_dict = variables[current_scope]
    alfa = VariableDetails(current_type, get_var_mem(current_scope, current_type, totalSize), arrayDetails)
    #aux_dict[current_function['id']][current_id] = alfa
    aux_dict[current_function['id']][idstack.top()] = alfa
  current_type = ''
  current_id = ''
  idstack.pop()
  #checkstack.pop()
  arrayDetails.erase()
  r = 1
  # print('DECLARATION')

def p_register_dimensions(t):
    'register_dimensions : '
    global r, totalSize, arrayDetails
    #print("Array dimensions: ", current_id, " : ", r)
    totalSize = r
    #print(isArray)
    #if(isArray[current_id]):
    if(isArray[idstack.top()]):
        for det in arrayDetails.details:
            r = int(r / det.size)
            det.set_m(r)
        #for det in arrayDetails.details:
        #    print("[size, m][", det.size, ",", det.m, "]")

def p_expresion(t):
    'expresion : level3 expresion_loop'
    #print('EXPRESION: ')
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
  'void_fun_call : ID_FUN check_void_fun_call L_PAREN add_bottom fun_call_opts R_PAREN fun_call_quadruples'

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
  'fun_call : ID_FUN save_fun_id L_PAREN add_bottom fun_call_opts R_PAREN remove_bottom fun_call_quadruples'
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
  reset_mem_counter(current_function)
  # reset_current_function()
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
            | variable idstackpop
            | fun_call guadalupean_patch'''
  #print('LEVEL0')

def p_idstackpop(t):
    'idstackpop : '
    global idstack
    idstack.pop()
    checkstack.pop()

def p_guadalupean_patch(t):
  '''guadalupean_patch : '''
  guadalupean_patch()

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
  reset_mem_counter(current_function)
  tempQuad.build(operations['EPROG'], None, None, None)
  QuadrupleList.push(tempQuad)
  # print('MAIN')

def p_set_main_function(t):
  '''set_main_function : '''
  global current_function, variables, current_scope
  mainQuad = QuadrupleList.quadruple_list[0]
  mainQuad.result = QuadrupleList.next_quadruple
  current_function['id'] = 'main'
  current_function['type'] = 'void'
  current_function['params_types'] = []
  current_function['params_ids'] = []
  current_function['mem_needed'] = []
  # variables['function']['main'] = {}
  add_to_fun_dict()
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
  global current_id, current_function, idstack
  #current_function['params_ids'].append(current_id)
  current_function['params_ids'].append(idstack.top())
  # print('Appended', current_id, 'to current_function[params_ids]')
  current_id = ''
  idstack.pop()
  checkstack.pop()
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
  'repeat : REPEAT L_PAREN add_bottom INT_CONST get_repeat_iterations R_PAREN remove_bottom block finish_repeat'
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
  'variable : ID set_variable opt_array'
  #print('VARIABLE')

def p_set_variable(t):
  'set_variable : '
  global current_id, variables, checked_variable, dim, checked_dimension, idstack
  dim = 0
  checked_variable = 0
  checked_dimension = 0
  current_id = t[-1] # Set variable id as current_id
  idstack.push(t[-1])
  checkstack.push(0)
  operands.push(t[-1]) # Push literal variable id to operands stack
  #current_id = t[1] # Set variable id as current_id
  #operands.push(t[1]) # Push literal variable id to operands stack
  # types.push(type(t[1])) # Push variable type to types stack
  #print('SETTING ',t[-1])

def p_opt_array(t):
  '''opt_array : empty
               | check_dimensions dimensions calculate_location'''
  #print('OPT ARRAY')

def p_calculate_location(t):
    'calculate_location : '
    calculate_location()

def p_dimensions(t):
  'dimensions : L_BRACKET expresion evaluate_index R_BRACKET dim_loop'
  #print('DIMENSIONS')

def p_dim_loop(t):
    '''dim_loop : dimensions
                | empty'''
    global dim
    dim += 1
    # print('DIM LOOP')

def p_check_dimensions(t):
    'check_dimensions : '
    check_dimensions()

def p_evaluate_index(t):
    'evaluate_index : '
    validate_quadruple()

def p_variable_decl(t):
  'variable_decl : ID set_false opt_array_decl'
  operands.push(t[1]) # Push literal variable id to operands stack
  # types.push(type(t[1])) # Push variable type to types stack
  # print('VARIABLE')

def p_set_false(t):
    'set_false : '
    global isArray, current_id, idstack
    current_id = t[-1] # Set variable id as current_id
    idstack.push(t[-1])
    #isArray[current_id] = False
    isArray[idstack.top()] = False

def p_opt_array_decl(t):
  '''opt_array_decl : empty
                    | start_array dimensions_decl'''
  # print('OPT ARRAY')

def p_dimensions_decl(t):
  'dimensions_decl : L_BRACKET INT_CONST declare_dimension R_BRACKET dim_loop_decl'
  # print('DIMENSIONS')

def p_dim_loop_decl(t):
  '''dim_loop_decl : dimensions_decl
                   | empty'''
  # print('DIM LOOP')

def p_declare_dimension(t):
    'declare_dimension :'
    global arrayDetails, r, dim
    arrayDetails.add_details(Details(t[-1]))
    r = t[-1] * r
    dim += 1

def p_start_array(t):
    'start_array : '
    start_array()

def p_vfunction(t):
  'vfunction : VOID set_fun_void L_PAREN opt_params R_PAREN block'
  # print('VFUNCTION')

def p_set_fun_void(t):
  '''set_fun_void : '''
  global current_function
  current_function['type'] = 'void'
  # print('Current function type: ', current_function['type'])

def p_while(t):
  'while : WHILE L_PAREN add_bottom expresion while_quadruple R_PAREN remove_bottom block complete_while_quadruple'
  # print('WHILE')

def p_while_quadruple(t):
  '''while_quadruple : '''
  while_quadruple()

def p_complete_while_quadruple(t):
  '''complete_while_quadruple : '''
  complete_while_quadruple()

def p_write(t):
    #TODO writes with parenthesis in the expression don't work
  'write : WRITE L_PAREN add_bottom write_opt R_PAREN remove_bottom'
  # print('WRITE')

def p_write_opt(t):
  '''write_opt : expresion write_expression
               | STRING_CONST add_string_const'''
  # print('WRITE OPT')

def p_write_expression(t):
    'write_expression : '
    #print(t[-1], "::::::")
    write_expression_quadruple()
    # QuadrupleList.print()
    # print('WRITE EXPRESSION')

def p_add_string_const(t):
  '''add_string_const : '''
  global constants
  cons_mem = append_const(t[-1], 'string') # Get virtual memory of hash
  tmpQuad = Quadruple()
  tmpQuad.build(operations['WRITE'], None, None, cons_mem)
  QuadrupleList.push(tmpQuad)

# Function used to print variables saved
def p_print_everything(t):
  '''print_everything : '''
  global variables, functions, constants, constants_memory
  print('Variables')
  for x in variables:
    print (x)
    for y in variables[x]:
        print (y,':',variables[x][y])
        #print (y,':',variables[x][y],':',variables[x][y].vmemory)
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
levels = {  1:2, # +
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
      QuadrupleList.print()
      print('Syntax error in ', p.value, ' at line ', p.lineno)
      p.lineno = 0
      exit(0)

####################
# Helper functions #
####################

def make_positive(x):
    if x < 0:
        x *= -1
    return x

def calculate_location():
    global tempCount, variables, current_function, current_id, idstack
    #base_dir = get_operand_mem(current_id, current_function) # Gets memory for the variable
    base_dir = get_operand_mem(idstack.top(), current_function) # Gets memory for the variable
    cons_mem = append_const(base_dir, 'int') # Get virtual memory for the base direction
    aux = operands.pop()
    if(typeString(str(type(aux))) == 'str'): # Check if aux is a variable
      aux = get_operand_mem(aux, current_function) # Gets memory for the variable
    sum_code = operations['+']
    tempQuad = Quadruple()
    #generate temp
    newid = 'tmp' + str(tempCount)
    tempCount += 1
    newid_type = string_types[1]
    tmp_mem = get_var_mem(current_scope, newid_type) * -1
    aux_dict = variables[current_scope] # Line used to reduce next's line length
    aux_dict[current_function['id']][newid] = VariableDetails(newid_type, tmp_mem) # Saves tmp in variables hash under current_function 
    #
    tempQuad.build(sum_code, aux, cons_mem, tmp_mem)
    QuadrupleList.push(tempQuad)
    #QuadrupleList.print()
    operators.pop()
    operands.push(newid)
    #print("THIS IS THE LAST:" ,operators.top())

def start_array():
    global arrayDetails, isArray, dim, r, idstack
    arrayDetails = ArrayDetails()
    #print(isArray)
    #isArray[current_id] = True
    isArray[idstack.top()] = True
    #print(isArray)
    dim = 1
    r = 1

def check_dimensions():
    global dim, var, isArray, current_id, idstack
    operand_id = operands.pop()
    #if current_id in variables['function'][current_function['id']]:
    if idstack.top() in variables['function'][current_function['id']]:
        #var_det = variables['function'][current_function['id']][current_id]
        var_det = variables['function'][current_function['id']][idstack.top()]
    else :
        #var_det = variables['global'][current_id]
        var_det = variables['global'][idstack.top()]
    #if not isArray[current_id]:
    if not isArray[idstack.top()]:
        print("Error, variable ", operand_id, " is not an array.")
    #dim = 0
    operators.push(operations['('])

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

def validate_quadruple():
    global current_function, checked_dimension, dim, tempCount, current_id, idstack
    dim += 1
    tempQuad = Quadruple()
    index = operands.top()
    verify_code = operations['VERIFY']
    multiply_code = operations['*']
    sum_code = operations['+']

    if(typeString(str(type(index))) == 'str'):
        if(index not in variables['function'][current_function['id']]):
            if(index not in variables['global']):
                print('Operand ', index, ' has not been defined.')
            else:
                op_det = variables['global'][index]
                op_type = op_det.vtype
                index = op_det.vmemory
        else:
            op_det = variables['function'][current_function['id']][index]
            op_type = op_det.vtype
            index = op_det.vmemory

    #var = get_operand_mem(current_id, current_function) # Gets memory for the variable
    var = get_operand_mem(idstack.top(), current_function) # Gets memory for the variable
    #TODO validations for missing variable
    # right now, it assumes the variable exists
    #if current_id in variables['function'][current_function['id']]:
    if idstack.top() in variables['function'][current_function['id']]:
        #var_det = variables['function'][current_function['id']][current_id]
        var_det = variables['function'][current_function['id']][idstack.top()]
    else :
        #var_det = variables['global'][current_id]
        var_det = variables['global'][idstack.top()]
    size = var_det.arrayDetails.details[checkstack.top()].size
    m = var_det.arrayDetails.details[checkstack.top()].m
    cons_mem = append_const(m, 'int') # Get virtual memory for m
    #checked_dimension += 1
    checkstack.push(checkstack.pop()+1)
    #before_last = checked_dimension < var_det.arrayDetails.totalSize
    before_last = checkstack.top() < var_det.arrayDetails.totalSize
    print(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ", before_last, checkstack.top(), var_det.arrayDetails.totalSize)

    # Generate validation quadruple
    tempQuad.build(verify_code, index, 0, size)
    QuadrupleList.push(tempQuad)

    # If there are more dimensions to check
    if before_last:
        tempQuad = Quadruple()
        aux = operands.pop()
        if(typeString(str(type(aux))) == 'str'): # Check if aux is a variable
            aux = get_operand_mem(aux, current_function) # Gets memory for the variable
        #generate temp
        newid = 'tmp' + str(tempCount)
        tempCount += 1
        newid_type = string_types[1]
        tmp_mem = get_var_mem(current_scope, newid_type)
        #
        tempQuad.build(multiply_code, aux, cons_mem, tmp_mem)
        QuadrupleList.push(tempQuad)
        operands.push(tmp_mem)
    # If we are on the 2nd or greater dimension
    if checkstack.top() > 1:
        tempQuad = Quadruple()
        aux2 = operands.pop()
        aux1 = operands.pop()
        if(typeString(str(type(aux1))) == 'str'): # Check if aux1 is a variable
            aux1 = get_operand_mem(aux1, current_function) # Gets memory for the variable
        if(typeString(str(type(aux2))) == 'str'): # Check if aux2 is a variable
            aux2 = get_operand_mem(aux2, current_function) # Gets memory for the variable
        #generate temp
        newid = 'tmp' + str(tempCount)
        tempCount += 1
        newid_type = string_types[1]
        tmp_mem = get_var_mem(current_scope, newid_type)
        #
        tempQuad.build(sum_code, aux1, aux2, tmp_mem)
        print(sum_code, aux1, aux2, tmp_mem, " <-----------------")
        QuadrupleList.push(tempQuad)
        operands.push(tmp_mem)

def write_expression_quadruple():
    tempQuad = Quadruple()
    lastQuad = QuadrupleList.get_last()
    operand = operands.pop()
    if(typeString(str(type(operand))) == 'str'): # Check if operand is a variable
      operand = get_operand_mem(operand, current_function) # Gets memory for the variable
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
    global current_function, variables, semantic_cube
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
          print('Type mismatch in assignment to ', ass_variable)
          exit(0)
        tempQuad.build(operation, operand, None, variables['global'][ass_variable].vmemory)
        QuadrupleList.push(tempQuad)
    else:
      #########################################################################3
      if(typeString(str(type(operand))) == 'str'):
        if(operand not in variables['function'][current_function['id']]):
          if(operand not in variables['global']):
            print('Operand ', operand, ' has not been defined.')
          else:
            op_det = variables['global'][operand]
            op_type = op_det.vtype
            operand = op_det.vmemory
        else:
          op_det = variables['function'][current_function['id']][operand]
          op_type = op_det.vtype
          operand = op_det.vmemory
      else:
        op_type = memory_to_data_type(operand)
      ####################################################################333
      var_det = variables['function'][current_function['id']][ass_variable]
      var_type = var_det.vtype
      if(semantic_cube[int_types[op_type]][int_types[var_type]][operation] == -1):
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

    type1 = memory_to_data_type(make_positive(operand1)) # Get type of variable/constant given the memory slot
    type2 = memory_to_data_type(make_positive(operand2))

    #QuadrupleList.print()
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
  tempQuad.build(operations['goto'], None, None, QuadrupleList.jump_stack.top() - 1) # Set jump to check while condition again
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
    return_val = get_operand_mem(return_val, current_function) # Gets local memory for the variable
  val_type = memory_to_data_type(return_val)

  # Semantic evaluation
  if(current_function['type'] != val_type):
    print('Function ', current_function['id'], ' expecting return value type \'', current_function['type'], '\', but got \'', val_type, '\'')
    exit(0)

  # Create global variable
  if(current_function['id'] not in variables['global']):
    print('Crea una variable global con nombre ', current_function['id'])
    global_var_type = current_function['type']
    global_var_mem = get_var_mem('global', global_var_type)
    trickQuad = Quadruple()
    trickQuad.build(operations['='], return_val, None, global_var_mem)
    QuadrupleList.push(trickQuad)
    variables['global'][current_function['id']] = VariableDetails(global_var_type, global_var_mem)
    operands.push(current_function['id'])
  else:
    print('Modifica memoria ya creada con el nombre ', current_function['id'])
    global_var_det = variables['global'][current_function['id']]
    global_var_mem = global_var_det.vmemory
    trickQuad = Quadruple()
    trickQuad.build(operations['='], return_val, None, global_var_mem)
    QuadrupleList.push(trickQuad)
    operands.push(current_function['id'])

  tempQuad = Quadruple()
  tempQuad.build(operations['RET'], None, None, global_var_mem)
  QuadrupleList.push(tempQuad)

  tempQuad2 = Quadruple()
  tempQuad2.build(operations['EPROC'], None, None, None)
  QuadrupleList.push(tempQuad2)

  # reset_mem_counter(current_function)
  # reset_current_function()

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
  # current_fun_call = ''
  # fun_call_params = []

def guadalupean_patch():
  # var_id = operands.pop() # Gets function_id pushed in return quadruple function
  global current_fun_call, fun_call_params
  var_det = variables['global'][current_fun_call]
  global_var_mem = var_det.vmemory # Gets global memory where value was saved
  # Generate tmp to assign return value in local scope and push it to operands
  local_var_mem = get_var_mem('function', var_det.vtype)
  operands.push(local_var_mem)
  # Make assign quadruple and push it to list
  tmpQuad = Quadruple()
  tmpQuad.build(operations['='], global_var_mem, None, local_var_mem)
  QuadrupleList.push(tmpQuad)

  # Reset all memory used to generate quadruples
  #current_fun_call = ''
  fun_call_params = []

def check_fun_call_exist(id_fun):
  global functions
  return id_fun in functions

memoryStack = zStack()

def get_scope(memAddress):
  if(memAddress >= 18000):
    print('Memory segment overflow')
    exit(0)
  if(memAddress < 6000):
    return 0 #global
  elif(memAddress < 12000):
    return 1 #constant
  elif(memAddress < 18000):
    return 2 #local

def get_sublist(memAddress):
  # print('memadress: ', memAddress)
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
  global global_memory, function_memory, constants_memory, zombie_memory
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
      return constants_memory[2][memAddress-9000]
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
  global global_memory, function_memory, constants_memory, zombie_memory
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

# Returns [scope, data_type, real mem address]
def get_real(x):
    global variables
    if x >= 0:
        return x
    x *= -1
    return get_value(x)

#def get_address(x):
def make_magic():
  global global_memory, function_memory, constants_memory, zombie_memory
  i = 0
  while(True):
    #print('i: ', i)
    #print('Global memory', global_memory)
    #print('Constants memory', constants_memory)
    #print('Local memory', function_memory)
    #print('Memory stack size: ', memoryStack.size())
    quad = QuadrupleList.quadruple_list[i]
    if(quad.operator == 1): # +
      # global i
      if quad.result < 0:
          resultAddr = get_address(-1 * quad.result) # Gets array scope, type, real mem address
      else:
          resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' + ', op2)
      res = op1 + op2
      function_memory[resultAddr[1]][resultAddr[2]] = res
      i += 1
    elif(quad.operator == 2): # -
      # global i
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' - ', op2)
      res = op1 - op2
      function_memory[resultAddr[1]][resultAddr[2]] = res
      i += 1
    elif(quad.operator == 3): # *
      # global i
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' * ', op2)
      res = op1 * op2
      function_memory[resultAddr[1]][resultAddr[2]] = res
      i += 1
    elif(quad.operator == 4): # /
      # global i
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' / ', op2)
      res = op1 / op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      i += 1
    elif(quad.operator == 5): # %
      # global i
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' % ', op2)
      res = op1 % op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      i += 1
    elif(quad.operator == 6): # =
      # global i
      resultAddr = get_address(get_real(quad.result)) # Gets array scope, type, real mem address
      if(resultAddr[0] == 0): # If scope is global
        global_memory[resultAddr[1]][resultAddr[2]] = get_value(get_real(quad.left))
      elif(resultAddr[0] == 1):
        constants_memory[resultAddr[1]][resultAddr[2]] = get_value(get_real(quad.left))
      else:
        function_memory[resultAddr[1]][resultAddr[2]] = get_value(get_real(quad.left))
      #print('= ', get_value(get_real(quad.left)))
      i += 1
    elif(quad.operator == 7): # ==
      # global i
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' == ', op2)
      res = op1 == op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      i += 1
    elif(quad.operator == 8): # >
      # global i
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' > ', op2)
      res = op1 > op2
      function_memory[resultAddr[1]][resultAddr[2]] = res
      i += 1
    elif(quad.operator == 9): # <
      # global i
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' < ', op2)
      res = op1 < op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      i += 1
    elif(quad.operator == 10): # <=
      # global i
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' <= ', op2)
      res = op1 <= op2
      function_memory[resultAddr[1]][resultAddr[2]] = res
      i += 1
    elif(quad.operator == 11): # >=
      # global i
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' >= ', op2)
      res = op1 >= op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      i += 1
    elif(quad.operator == 12): # <>
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' <> ', op2)
      res = op1 != op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      i += 1
    elif(quad.operator == 13): # &&
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' && ', op2)
      res = op1 and op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      i += 1
    elif(quad.operator == 14): # ||
      resultAddr = get_address(quad.result) # Gets array scope, type, real mem address
      op1 = get_value(get_real(quad.left))
      op2 = get_value(get_real(quad.right))
      #print(op1, ' || ', op2)
      res = op1 or op2
      function_memory[resultAddr[1]][resultAddr[2]] = res 
      i += 1
    elif(quad.operator == 15): # (
      print("(")
    elif(quad.operator == 16): # )
      print(")")
    elif(quad.operator == 17): # goto
      # global i
      i = quad.result
      #print('goto: ', i)
    elif(quad.operator == 18): # gotof
      # global i
      resultAddr = get_address(quad.left)
      # Aqui está el print de la listita
      #print(resultAddr)
      if(resultAddr[0] == 0): # If scope is global
        if(global_memory[resultAddr[1]][resultAddr[2]] != True):
           i = quad.result
        else:
          i += 1
      elif(resultAddr[0] == 1):
        if(constants_memory[resultAddr[1]][resultAddr[2]] != True):
           i = quad.result
        else:
          i += 1
      elif(resultAddr[0] == 2):
        if(function_memory[resultAddr[1]][resultAddr[2]] != True):
          i = quad.result
        else:
          i += 1
      #print("gotof", i)
    elif(quad.operator == 19): # gotoz
      # global i
      if(quad.left == 0):
        i = quad.result
      else:
        i += 1
      #print("gotoz", i)
    elif(quad.operator == 20): # READ
      # global i
      print("READ")
    elif(quad.operator == 21): # WRITE
      # global i
      #print(quad.result)
      print(get_value(get_real(quad.result)))
      #print("WRITE")
      i += 1
    elif(quad.operator == 22): # RET
      # global i
      i += 1
      #print("RET ", quad.result)
    elif(quad.operator == 23): # EPROC
      # global i
      #print("EPROC")
      mem = memoryStack.pop()
      function_memory = mem.memory
      #print('Recoverded memory: ', mem.memory)
      i = mem.last_quadruple
      #print('Returning to ', i)
    elif(quad.operator == 24): # EPROG
      # global i
      print('Program terminated')
      exit(0)
      # print("EPROG")
    elif(quad.operator == 25): # DIM
      # global i
      QuadrupleList.quadruple_list[i].left -= 1
      i += 1
      #print("DIM")
    elif(quad.operator == 26): # PARAM
      # global i
      tmpAddr = get_address(quad.left)
      zombie_memory[tmpAddr[1]][tmpAddr[2]] = get_value(quad.result)
      i += 1
      #print('PARAM', get_value(quad.result))
    elif(quad.operator == 27): # gosub
      # global i
      mem = Memory()
      mem.build(function_memory, i+1)
      #print('GOSUB, SAVING MEMORY: ', function_memory)
      memoryStack.push(mem)
      function_memory = zombie_memory
      #print('New local memory = ', function_memory)
      reset_zombie_mem()
      i = quad.result
    elif(quad.operator == 28): # ERA
      # global i
      make_zombie_mem(quad.result)
      i += 1
      #print("ERA callling ", quad.result)
    elif(quad.operator == 29): # VERIFY
      # global i
      op = get_value(quad.left)
      #if op >= quad.result:
      #    print("Array index out of bounds (greater) at ", get_value(quad.left), ">=", op, " (", quad.left, ")")
      #    exit(1)
      #if op < quad.right:
      #    print("Array index out of bounds (less than) at ", get_value(quad.right), " (", quad.right, ")")
      #    exit(1)
      i += 1

def make_zombie_mem(fun_name):
  global zombie_memory
  fun_det = functions[fun_name]
  mem_needed = fun_det.mem_needed
  # print(mem_needed)
  zombie_memory[0] = [None] * mem_needed[0]
  zombie_memory[1] = [None] * mem_needed[1]
  zombie_memory[2] = [None] * mem_needed[2]
  zombie_memory[3] = [None] * mem_needed[3]

def reset_zombie_mem():
  global zombie_memory
  zombie_memory = [[] for i in range(4)]

parser = yacc.yacc()
file = open("inputs/matrix_mult.zm", "r")
yacc.parse(file.read())
file.close()
