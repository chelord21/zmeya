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
types = zStack()
tempQuad = Quadruple()
#arithmetic
tempCount = 1

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
  'assignment : variable EQUALS assignment_opts'
  # print('ASSIGNMENT')

def p_assignment_opts(t):
  '''assignment_opts : expresion'''
  # print('ASSIGNMET OPTS')

def p_atomic(t):
  '''atomic : STRING
            | INT
            | FLOAT
            | BOOL'''
  global current_type
  current_type = t[1]
  print('Current type: ', current_type)
  # print('ATOMIC')

def p_block(t):
  'block : L_BRACE decl_kleen content_kleen R_BRACE'
  # print('BLOCK')

def p_condition(t):
  'condition : IF L_PAREN expresion R_PAREN if_quadruple oblock else_condition if_double_check'
  # print('CONDITION')

def p_if_quadruple(t):
  '''if_quadruple : '''
  if_quadruple()

def p_if_double_check(t):
  '''if_double_check : '''
  if_double_check()

def p_else_condition(t):
  '''else_condition : empty
                    | ELSE else_quadruple oblock else_finish_quad'''
  # print('ELSE CONDITION')

def p_else_quadruple(t):
  '''else_quadruple : '''
  else_quadruple()

def p_else_finish_quad(t):
  '''else_finish_quad : '''
  esle_finish_quadruple()

def p_constant(t):
  '''constant : INT_CONST
              | FLOAT_CONST
              | TRUE
              | FALSE'''
  global constants
  constants[t[1]] = type(t[1])
    # arithmetic
  operands.push(t[1])
  print(operands.top())
  types.push(type(t[1]))
  #print('CONSTANT: ' + str(t[1]))

def p_content(t):
  '''content : sentence
             | loops
             | condition'''
  # print('CONTENT')

def p_declaration(t):
  'declaration : VAR variable COLON atomic SEMICOLON'
  global current_scope, current_type, current_id, current_function
  print('Saving variable in scope: ', current_scope)
  if current_scope == 'global':
    variables[current_scope][current_id] = VariableDetails(current_type)
    print('Saved in variables[', current_scope, '][', current_id, ']')
    current_type = ''
    current_id = ''
    print('Current id after save: ', current_id)
    print('Current id after type: ', current_type)
  else:
    variables[current_scope][current_function['id']][current_id] = VariableDetails(current_type)
    current_type = ''
    current_id = ''
  # print('DECLARATION')

def p_dimensions(t):
  'dimensions : L_BRACKET POS_INT_CONST R_BRACKET dim_loop'
  # print('DIMENSIONS')

def p_dim_loop(t):
  '''dim_loop : dimensions
              | empty'''
  # print('DIM LOOP')

def p_expresion(t):
  'expresion : level3 expresion_loop'
  print('EXPRESION: ')
  QuadrupleList.print()

def p_expresion_loop(t):
  '''expresion_loop : expresion_operations expresion
                    | empty'''
  # print('EXPRESION LOOP')

def p_expresion_operations(t):
    '''expresion_operations : OR
                            | AND'''
    push_operator(t)


def p_fun_call(t):
  'fun_call : ID_FUN L_PAREN fun_call_opts R_PAREN'
  # print('FUN CALL')

def p_fun_call_opts(t):
  '''fun_call_opts : empty
                   | expresion funcall_params_loop'''
  # print('FUN CALL OPTS')

def p_funcall_params_loop(t):
  '''funcall_params_loop : empty
                         | COMMA fun_call_opts'''
  # print('FUNCALL PARAMS LOOP')

def p_function(t):
  'function : ID_FUN set_fun_id COLON function_types reset_function'
  # print('FUNCTION')

def p_set_fun_id(t):
  '''set_fun_id : '''
  global current_function
  current_function['id'] = t[-1]
  print('Current function id: ', current_function['id'])

def p_reset_function(t):
  '''reset_function : '''
  reset_current_function()

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
  'main : MAIN block'
  # print('MAIN')

def p_oblock(t):
  'oblock : L_BRACE content_kleen oblock_opt R_BRACE'
  # print('OBLOCK')

def p_oblock_opt(t):
    '''oblock_opt : RETURN expresion SEMICOLON
                  | empty'''
    # print('OBLOCK_OPT')

def p_parameters(t):
  '''parameters : atomic set_param_type variable set_param_name params_loop'''
  # print('PARAMETERS')

# Append parameter type to the function's parameter types list
def p_set_param_type(t):
  '''set_param_type : '''
  global current_type, current_function
  current_function['params_types'].append(current_type)
  current_type = ''

# Append parameter id to the function's parameter names list
def p_set_param_name(t):
  '''set_param_name : '''
  global current_id, current_function
  current_function['params_ids'].append(current_id)
  current_id = ''

def p_params_loop(t):
  '''params_loop : COMMA parameters
                 | empty'''
  # print('PARAMS LOOP')

def p_rblock(t):
  'rblock : L_BRACE decl_kleen content_kleen RETURN expresion SEMICOLON R_BRACE'
  # print('RBLOCK')

def p_content_kleen(t):
  '''content_kleen : empty
                   | content content_kleen'''
  # print('CONTENT KLEEN')

def p_read(t):
  'read : READ L_PAREN variable R_PAREN'
  # print('READ')

def p_repeat(t):
  'repeat : REPEAT L_PAREN INT_CONST get_repeat_iterations R_PAREN block'
  # print('REPEAT')

def p_get_repeat_iterations(t):
  '''get_repeat_iterations : '''
  repeat_quadruple(t[-1])

def p_rfunction(t):
  'rfunction : atomic set_fun_type L_PAREN opt_params R_PAREN rblock'
  # print('RFUNCTION')

def p_set_fun_type(t):
  '''set_fun_type : '''
  global current_function, current_type
  current_function['type'] = current_type
  current_type = ''

# Add function with its details to function dictionary and change current scope
def p_opt_params(t):
  '''opt_params : empty
                | parameters'''
  add_to_fun_dict()
  # print('OPT PARAMS')

def p_sentence(t):
  '''sentence : assignment SEMICOLON
              | write SEMICOLON
              | read SEMICOLON
              | fun_call SEMICOLON'''
  # print('SENTENCE')

def p_variable(t):
  'variable : ID opt_array'
  global current_id
  current_id = t[1]
  print('Current id: ', current_id)
    # arithmetic
  operands.push(t[1])
  types.push(type(t[1]))
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
  print('Current function type: ', current_function['type'])

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
  'write : WRITE L_PAREN write_opt R_PAREN'
  # print('WRITE')

def p_write_opt(t):
  '''write_opt : expresion
               | STRING_CONST add_string_const'''
  # print('WRITE OPT')

def p_add_string_const(t):
  '''add_string_const : '''
  global constants
  constants[t[0]] = 'string'

# Function used to print variables saved
def p_print_everything(t):
  '''print_everything : '''
  global variables, functions, constants
  print('Variables')
  for x in variables:
    print (x)
    for y in variables[x]:
        print (y,':',variables[x][y])
  print('Fucntions')
  for x in functions:
    print (x)
  print('Constants')
  for x in constants:
    print (x)

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
      # print('Syntax error')
      exit(0)
    else:
      # print('Syntax error in ', p.value, ' at line ', p.lineno)
      p.lineno = 0
      exit(0)

# Helper functions
def get_type_from_stack():
    return str(types.pop()).split("'")[1]

def push_operator(t):
    operators.push(operations[t[1]])

##################################
# Quadruple generation functions #
##################################

def arithmetic_quadruple():
    global tempCount
    tempQuad = Quadruple()
    type2 = get_type_from_stack()
    type1 = get_type_from_stack()

    print(":: Types2: ", type2, "::", int_types[type2])
    print(":: Types1: ", type1, "::", int_types[type1])
    operator = operators.pop()
    operand2 = operands.pop()
    operand1 = operands.pop()
    print(":: Operand2: ", operand2)
    print(":: Operand1: ", operand1)
    result = 'temp' + str(tempCount)
    tempCount += 1
    tempQuad.build(operator, operand1, operand2, result)
    QuadrupleList.push(tempQuad)
    operands.push(result)
    types.push(type(result))

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
  # Debug
  # print('---------WHILE COMPLETION CHECK---------')
  # QuadrupleList.print()

# Generates quadruple for repeat loop
def repeat_quadruple(iterations):
  # TODO: Save new variable in memory with the constant value of iterations
  # e.g. memory[5000+offset] = iterations
  # Generate new cuadruple

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
  # Debug
  # print('-----IF GENERATION CHECK-----')
  # QuadrupleList.print()

# Else encountered. Complete corresponding if quadruple and generate goto quadruple
def else_quadruple():
  complete_if()
  jumps = QuadrupleList.jump_stack # Get jump stack from QuadrupleList class
  jumps.push(QuadrupleList.next_quadruple) # Push next_quadruple to jumps stack to keep track
  tempQuad = Quadruple()
  tempQuad.build(operations['goto'], None, None, None) # Generate goto quadruple
  QuadrupleList.push(tempQuad) # Push it to quadruples list
  # Debug
  # print('-----ELSE CHECK-----')
  # QuadrupleList.print()

# Completes corresponding if quadruple because block ended or else found
def complete_if():
  quadIndex = QuadrupleList.jump_stack.pop() # Get the index of corresponding if quadruple to complete
  ifQuad = QuadrupleList.quadruple_list[quadIndex] # Get the quadruple
  ifQuad.result = QuadrupleList.next_quadruple # Asign next quadruple to quadruple's result
  # Debug
  # print('-----IF COMPLETION CHECK-----')
  # QuadrupleList.print()

# Check if IF quadruple was completed by an else, if not, completed by end of block
def if_double_check():
  if(QuadrupleList.jump_stack.size() > 0):
    quadIndex = QuadrupleList.jump_stack.pop() # Get the index of corresponding if quadruple to complete
    ifQuad = QuadrupleList.quadruple_list[quadIndex] # Get the quadruple
    if(ifQuad.result is None): # If IF quadruple is not completed yet by an else token, complete if by end of block
      complete_if()
    # Debug
    # print('-----IF DOUBLE CHECK-----')
    # QuadrupleList.print()

def esle_finish_quadruple():
  quadIndex = QuadrupleList.jump_stack.pop() # Get the index of corresponding if quadruple to complete
  elseQuad = QuadrupleList.quadruple_list[quadIndex] # Get the quadruple
  elseQuad.result = QuadrupleList.next_quadruple # Asign next quadruple to quadruple's result
  # Debug
  # print('-----ELSE COMPLETION CHECK-----')
  # QuadrupleList.print()

parser = yacc.yacc()
file = open("inputs/conditions.zm", "r")
yacc.parse(file.read())
file.close()
