# -*- coding: utf-8 -*-
# Analizador sintáctico de ViLe
# Marcel Benítez Martínez 1139855
# Abraham Rodríguez 1195653

import ply.yacc as yacc
import lexer

tokens= lexer.tokens

def p_program(t):
  '''programm : function program
              | main'''

def p_function(t):
  'function : FUN type L_PAREN function_aux R_PAREN block'

def p_function_aux(t):
  '''function_aux : vars
                  | empty'''

def p_main(t):
  'main : MAIN block'

def p_type(t):
  '''type : STRING
          | INT
          | FLOAT
          | CHAR
          | BOOL'''

def p_vars(t):
  '''vars : empty
          | type ID var_aux SEMICOLON vars'''

def p_var_aux(t):
  '''var_aux : empty
             | COMMA ID var_aux'''

def p_block(t):
  'block : L_BRACE block_aux RETURN R_BRACE'

def p_block_aux(t):
  '''block_aux : empty
               | sentence'''

def p_sentence(t):
  '''sentence : assignment
              | condition
              | write
              | read
              | for
              | while'''

def p_assignment(t):
  'assignment : ID EQUALS expresion SEMICOLON'

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
  'level3 : level2 logical level2'

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

def p_logical(t):
  '''logical : L_EQUAL
             | G_EQUAL
             | LESS
             | GREATER
             | N_EQUAL'''

def p_read(t):
  'read : READ L_PAREN ID R_PAREN SEMICOLON'

def p_write(t):
  'write : WRITE L_PAREN write_aux R_PAREN SEMICOLON'

def p_write_aux(t):
  '''write_aux : STRING
               | expresion'''

def p_repeat(t):
  'repeat : FOR L_PAREN assi cond exec R_PAREN block'

def p_while(t):
  'while : WHILE L_PAREN expresion R_PAREN block'

def p_assi(t):
  'assi : ID EQUALS INTCONST SEMICOLON'

def p_cond(t):
  'cond : ID logical ID SEMICOLON'

def p_exec(t):
  'exec : assignment'

def p_constant(t):
  '''constant : ID
              | INT_CONST
              | FLOAT_CONST
              | TRUE
              | FALSE'''

def p_vector(t):
  'vector : VECTOR type ID'

def p_empty(p):
    'empty :'
    pass

parser = yacc.yacc()