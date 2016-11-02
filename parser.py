# -*- coding: utf-8 -*-
# Analizador sintáctico de Zmeya
# Marcelo Salcedo A01195804
# Sergio Cordero a01191167

import ply.yacc as yacc
import lexer

tokens= lexer.tokens

def p_program(t):
  'program : decl_kleen function_kleen main'
  print('PROGRAM')

def p_decl_kleen(t):
  '''decl_kleen : empty
                | declaration decl_kleen'''
  print('DECL KLEEN')

def p_function_kleen(t):
  '''function_kleen : empty
                    | function function_kleen'''
  print('FUNCTION KLEEN')

def p_arr_declaration(t):
  'arr_declaration : atomic ID dimensions'
  print('ARR DECLARATION')

def p_assignment(t):
  'assignment : variable EQUALS assignment_opts'
  print('ASSIGNMENT')

def p_assignment_opts(t):
  '''assignment_opts : expresion
                     | fun_call'''
  print('ASSIGNMET OPTS')

def p_at_declaration(t):
  'at_declaration : atomic ID'
  print('AT DECLARATION')

def p_atomic(t):
  '''atomic : STRING
             | INT
             | FLOAT
             | CHAR
             | BOOL'''
  print('ATOMIC')

def p_block(t):
  'block : L_BRACE decl_kleen content R_BRACE'
  print('BLOCK')

def p_condition(t):
  'condition : IF L_PAREN expresion R_PAREN block else_condition'
  print('CONDITION')

def p_else_condition(t):
  '''else_condition : empty
                    | ELSE block'''
  print('ELSE CONDITION')

def p_constant(t):
  '''constant : INT_CONST
              | FLOAT_CONST
              | TRUE
              | FALSE'''
  print('CONSTANT')

def p_content(t):
  '''content : sentence
             | loops
             | condition'''
  print('CONTENT')

def p_declaration(t):
  '''declaration : at_declaration SEMICOLON
                 | arr_declaration SEMICOLON'''
  print('DECLARATION')

def p_dimensions(t):
  'dimensions : L_BRACKET POS_INT_CONST R_BRACKET dim_loop'
  print('DIMENSIONS')

def p_dim_loop(t):
  '''dim_loop : dimensions
              | empty'''
  print('DIMENSION LOOP')

def p_expresion(t):
  'expresion : level3 expresion_loop'
  print('EXPRESION')

def p_expresion_loop(t):
  '''expresion_loop : OR expresion
                    | AND expresion
                    | empty'''
  print('EXPRESION LOOP')

def p_fun_call(t):
  'fun_call : ID L_PAREN fun_call_opts R_PAREN'
  print('FUN CALL')

def p_fun_call_opts(t):
  '''fun_call_opts : empty
                   | expresion funcall_params_loop'''
  print('FUN CALL OPTS')

# def p_funcall_params(t):
#   '''funcall_params : expresion
#                     | variable'''

def p_funcall_params_loop(t):
  '''funcall_params_loop : empty
                         | COMMA fun_call_opts'''
  print('FUNCALL PARAMS LOOP')

def p_function(t):
  '''function : rfunction
              | vfunction'''
  print('FUNCTION')

def p_level0(t):
  '''level0 : L_PAREN expresion R_PAREN
             | constant
             | variable'''
  print('LEVEL0')

def p_level1(t):
  'level1 : level0 level1_loop'
  print('LEVEL1')

def p_level1_loop(t):
  '''level1_loop : empty
                 | MOD level1
                 | DIV level1
                 | MULT level1'''
  print('LEVEL1 LOOP')

def p_level2(t):
  'level2 : level1 level2_loop'
  print('LEVEL2')

def p_level2_loop(t):
  '''level2_loop : SUM level2
                 | MINUS level2
                 | empty'''
  print('LEVEL2 LOOP')

def p_level3(t):
  'level3 : level2 level3_loop'
  print('LEVEL3')

def p_level3_loop(t):
  '''level3_loop : empty
                 | relational level3'''
  print('LEVEL3 LOOP')

def p_loops(t):
  '''loops : while
           | repeat'''
  print('LOOPS')

def p_main(t):
  'main : MAIN rblock'
  print('MAIN')

def p_parameters(t):
  '''parameters : atomic variable params_loop'''
  print('PARAMETERS')

def p_params_loop(t):
  '''params_loop : COMMA parameters
                 | empty'''
  print('PARAMS LOOP')

def p_rblock(t):
  'rblock : L_BRACE decl_kleen content_kleen RETURN expresion SEMICOLON R_BRACE'
  print('RBLOCK')

def p_content_kleen(t):
  '''content_kleen : empty
                   | content content_kleen'''
  print('CONTENT KLEEN')

def p_read(t):
  'read : READ L_PAREN variable R_PAREN'
  print('READ')

def p_relational(t):
  '''relational : L_EQUAL
                | G_EQUAL
                | LESS
                | GREATER
                | N_EQUAL
                | EQUALITY'''
  print('RELATIONAL')

def p_repeat(t):
  'repeat : REPEAT L_PAREN POS_INT_CONST R_PAREN block'
  print('REPEAT')

def p_rfunction(t):
  'rfunction : atomic ID L_PAREN opt_params R_PAREN rblock'
  print('RFUNCTION')

def p_opt_params(t):
  '''opt_params : empty
                | parameters'''
  print('OPT PARAMS')

def p_sentence(t):
  '''sentence : assignment SEMICOLON
              | write SEMICOLON
              | read SEMICOLON
              | fun_call SEMICOLON'''
  print('SENTENCE')

def p_variable(t):
  'variable : ID opt_array'
  print('VARIABLE')

def p_opt_array(t):
  '''opt_array : empty
               | dimensions'''
  print('OPT ARRAY')

def p_vfunction(t):
  'vfunction : VOID ID L_PAREN opt_params R_PAREN block'
  print('VFUNCTION')

def p_while(t):
  'while : WHILE L_PAREN expresion R_PAREN block'
  print('WHILE')

def p_write(t):
  'write : WRITE L_PAREN write_opt R_PAREN'
  print('WRITE')

def p_write_opt(t):
  '''write_opt : expresion
               | STRING_CONST'''
  print('WRITE OPT')

def p_empty(p):
  'empty :'
  pass

def p_error(p):
  print("Syntax error in input!")

parser = yacc.yacc()
file = open("input.txt", "r")
yacc.parse(file.read())
file.close()