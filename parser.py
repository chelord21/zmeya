# -*- coding: utf-8 -*-
# Analizador sintáctico de ViLe
# Marcel Benítez Martínez 1139855
# Abraham Rodríguez 1195653

import ply.yacc as yacc
import lexer

tokens= lexer.tokens

def p_program(t):
  'programm : decl function_opt main'

def p_function_opt(t):
  '''function_opt : empty
                  | function function_opt'''

def p_function(t):
  'function : FUN type_opt L_PAREN function_aux R_PAREN block'

def p_type_opt(t):
  '''type_opt : type
              | VOID'''

def p_function_aux(t):
  '''function_aux : parameters
                  | empty'''

def p_main(t):
  'main : MAIN block'

def p_parameters(t):
  '''parameters : type params_aux params_loop'''

def p_params_aux(t):
  '''params_aux : ASAND ID
                | ID
                | a_variable'''

def p_params_loop(t):
  '''params_loop : COMMA parameters
                 | empty'''

def p_decl(t):
  '''decl : decl_aux SEMICOLON
          | empty'''

def p_decl_aux(t):
  '''decl_aux : at_declaration decl_loop
              | arr_declaration decl_loop'''

def p_decl_loop(t):
  '''decl_loop : COMMA decl_aux
               | empty'''

def p_nuclear(t):
  '''type : STRING
          | INT
          | FLOAT
          | CHAR
          | BOOL'''

def p_at_declaration(t):
  'at_declaration : nuclear ID'

def p_arr_declaration(t):
  'arr_declaration : nuclear ID dimensions'

def p_dimensions(t):
  'dimensions : L_BRACKET POS_INT_CONST R_BRACKET dim_loop'

def p_dim_loop(t):
  '''dim_loop : dimensions
              | empty'''

def p_block(t):
  'block : L_BRACE decl block_aux RETURN R_BRACE'

def p_block_aux(t):
  '''block_aux : empty
               | sentence'''

def p_sentence(t):
  '''sentence : assignment
              | condition
              | write
              | read
              | repeat
              | while'''

def p_repeat(t):
  'repeat : REPEAT L_PAREN POS_INT_CONST R_PAREN block'

def p_while(t):
  'while : WHILE L_PAREN expresion R_PAREN block'

def p_variable(t):
  '''variable : ID
              | arr_variable'''

def p_arr_variable(t):
  'arr_variable : ID av_loop'

def p_av_loop(t):
  'av_loop : L_BRACKET expresion R_BRACKET av_opt'

def p_av_opt(t):
  '''av_opt : empty
            | av_loop'''

def p_assignment(t):
  'assignment : variable EQUALS expresion SEMICOLON'

def p_read(t):
  'read : READ L_PAREN ID R_PAREN SEMICOLON'

def p_write(t):
  'write : WRITE L_PAREN write_opt R_PAREN SEMICOLON'

def p_write_opt(t):
  '''write_opt : expresion
               | STRING'''

def p_condition(t):
  'condition : IF L_PAREN expresion R_PAREN block condition_aux SEMICOLON'

def p_condition_aux(t):
  '''condition_aux : empty
                   | ELSE block'''

def p_expresion(t):
  'expresion : level3 expresion_aux'

def p_expresion_aux(t):
  '''expresion_aux : OR expresion
                   | AND expresion
                   | empty'''

def p_level3(t):
  'level3 : level2 relational level2'

def p_level2(t):
  'level2 : level1 level2_aux'

def p_level2_aux(t):
  '''level2_aux : SUM level2
                | MINUS level2
                | empty'''

def p_level1(t):
  'level1 : level0 level1_aux'

def p_level1_aux(t):
  '''level1_aux : empty
                | MOD level1
                | DIV level1
                | MULT level1'''

def p_level0(t):
  '''level_0 : L_PAREN expresion R_PAREN
             | constant
             | SUM constant
             | MINUS constant'''

def p_relational(t):
  '''logical : L_EQUAL
             | G_EQUAL
             | LESS
             | GREATER
             | N_EQUAL
             | EQUALITY'''

def p_constant(t):
  '''constant : variable
              | INT_CONST
              | FLOAT_CONST
              | TRUE
              | FALSE'''

def p_empty(p):
  'empty :'
  pass

def p_error(p):
  print("Syntax error in input!")

parser = yacc.yacc()