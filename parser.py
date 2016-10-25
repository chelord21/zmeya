# -*- coding: utf-8 -*-
# Analizador sintáctico de Zmeya
# Marcelo Salcedo A01195804
# Sergio Cordero a01191167

import ply.yacc as yacc
import lexer

tokens= lexer.tokens

def p_arr_declaration(t):
  'arr_declaration : atomic ID dimensions'

def p_arr_variable(t):
  'arr_variable : ID av_loop'

def p_av_loop(t):
  'av_loop : L_BRACKET expresion R_BRACKET av_opt'

def p_av_opt(t):
  '''av_opt : empty
            | av_loop'''

def p_assignment(t):
  'assignment : variable EQUALS expresion SEMICOLON'

def p_at_declaration(t):
  'at_declaration : atomic ID'

def p_atomic(t):
  '''atomic : STRING
             | INT
             | FLOAT
             | CHAR
             | BOOL'''

def p_block(t):
  'block : L_BRACE decl_loop sentence_loop RETURN SEMICOLON R_BRACE'

def p_sentence_loop(t):
  '''sentence_loop : sentence sentence_loop
                   | empty'''

def p_condition(t):
  'condition : IF L_PAREN expresion R_PAREN block condition_aux SEMICOLON'

def p_condition_aux(t):
  '''condition_aux : empty
                   | ELSE block'''

def p_constant(t):
  '''constant : variable
              | INT_CONST
              | FLOAT_CONST
              | TRUE
              | FALSE'''

def p_decl(t):
  '''decl : decl_aux
          | empty'''

def p_decl_aux(t):
  '''decl_aux : at_declaration decl_aux_loop
              | arr_declaration decl_aux_loop'''

def p_decl_aux_loop(t):
  '''decl_aux_loop : SEMICOLON decl_aux
               | empty'''

def p_dimensions(t):
  'dimensions : L_BRACKET POS_INT_CONST R_BRACKET dim_loop'

def p_dim_loop(t):
  '''dim_loop : dimensions
              | empty'''

def p_expresion(t):
  'expresion : level3 expresion_loop'

def p_expresion_loop(t):
  '''expresion_loop : OR expresion
                   | AND expresion
                   | empty'''

def p_function(t):
  '''function : rfunction
              | vfunction'''

def p_level0(t):
  '''level0 : L_PAREN expresion R_PAREN
             | constant
             | SUM constant
             | MINUS constant'''

def p_level1(t):
  'level1 : level0 level1_loop'

def p_level1_loop(t):
  '''level1_loop : empty
                | MOD level1
                | DIV level1
                | MULT level1'''

def p_level2(t):
  'level2 : level1 level2_aux'

def p_level2_aux(t):
  '''level2_aux : SUM level2
                | MINUS level2
                | empty'''

def p_level3(t):
  'level3 : level2 relational level2'

def p_main(t):
  'main : MAIN rblock'


def p_parameters(t):
  '''parameters : atomic params_aux'''

def p_params_aux(t):
  '''params_aux : ASAND ID params_loop
                | ID params_loop
                | arr_variable params_loop'''

def p_params_loop(t):
  '''params_loop : COMMA type params_aux
                 | empty'''

def p_program(t):
  'programm : decl_loop function_loop main'

def p_decl_loop(t):
  '''program_decl : empty
                  | decl decl_loop'''
def p_function_loop(t):
  '''function_opt : empty
                  | function program_funct'''

def p_rblock(t):
  'rblock : L_BRACE decl_loop sentence_loop RETURN expresion SEMICOLON R_BRACE'

def p_read(t):
  'read : READ L_PAREN variable R_PAREN SEMICOLON'

def p_relational(t):
  '''relational : L_EQUAL
                | G_EQUAL
                | LESS
                | GREATER
                | N_EQUAL
                | EQUALITY'''

def p_repeat(t):
  'repeat : REPEAT L_PAREN POS_INT_CONST R_PAREN block'

def p_rfunction(t):
  'rfunction : type ID L_PAREN opt_params R_PAREN block'

def p_opt_params(t):
  '''opt_params : empty
                | parameters'''

def p_sentence(t):
  '''sentence : assignment
              | condition
              | write
              | read
              | repeat
              | while'''

def p_variable(t):
  '''variable : ID
              | arr_variable'''

def p_vfunction(t):
  'vfunction : VOID ID L_PAREN opt_params R_PAREN rblock'

def p_while(t):
  'while : WHILE L_PAREN expresion R_PAREN block'

def p_write(t):
  'write : WRITE L_PAREN write_opt R_PAREN SEMICOLON'

def p_write_opt(t):
  '''write_opt : expresion
               | STRING'''

def p_empty(p):
  'empty :'
  pass

def p_error(p):
  print("Syntax error in input!")

parser = yacc.yacc()
