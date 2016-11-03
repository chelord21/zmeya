#
# -*- coding: utf-8 -*-
# Zmeya's Lexer
# José Marcelo Salcedo
# Sergio Jesús Cordero
#

import ply.lex as lex

# Reserved words
reserved = {
  'main'   : 'MAIN',
  'return' : 'RETURN',
  'if'     : 'IF',
  'else'   : 'ELSE',
  'write'  : 'WRITE',
  'read'   : 'READ',
  'while'  : 'WHILE',
  'repeat' : 'REPEAT',
  'int'    : 'INT',
  'float'  : 'FLOAT',
  'string' : 'STRING',
  'void'   : 'VOID',
  'bool'   : 'BOOL',
  'char'   : 'CHAR',
  'T'      : 'TRUE',
  'F'      : 'FALSE',
  '&&'     : 'AND',
  '||'     : 'OR'
}

tokens = [
  'SUM', 'MINUS','MULT', 'DIV', 'MOD', 'EQUALS',
  'EQUALITY', 'GREATER', 'LESS', 'L_EQUAL', 'G_EQUAL',
  'N_EQUAL', 'SEMICOLON', 'COMMA', 'L_PAREN', 'R_PAREN',
  'L_BRACE', 'R_BRACE', 'L_BRACKET', 'R_BRACKET', 'INT_CONST',
  'STRING_CONST', 'FLOAT_CONST', 'ID_FUN', 'ID', 'POS_INT_CONST',
  'COLON'
  ] + list(reserved.values())

# Token definitions
t_ignore = ' \t'
t_SUM = '\+'
t_MINUS = '-'
t_MULT = '\*'
t_DIV = '/'
t_MOD = '%'
t_EQUALS = '='
t_EQUALITY = '=='
t_GREATER = '>'
t_LESS = '<'
t_L_EQUAL = '<='
t_G_EQUAL = '>='
t_N_EQUAL = '<>'
t_SEMICOLON = ';'
t_COMMA = ','
t_L_PAREN = '\('
t_R_PAREN = '\)'
t_L_BRACE = '\{'
t_R_BRACE = '\}'
t_L_BRACKET = '\['
t_R_BRACKET = '\]'
t_COLON = ':'
t_INT_CONST = '[-][0-9]+'
t_POS_INT_CONST = '[0-9]+'
t_STRING_CONST = '"[a-zA-Z_].*"'
t_FLOAT_CONST = '[-]([0-9]+.)?[0-9]+'

# LOC counter
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID_FUN(t):
  '[_]+[a-zA-Z_][a-zA-Z0-9_]*'
  t.type = reserved.get(t.value, 'ID_FUN')
  return t

# ID recognition
# Checks if id is not a reserved word
def t_ID(t):
  '[a-zA-Z_][a-zA-Z0-9_]*'
  t.type = reserved.get(t.value, 'ID')
  return t

# Error
def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  exit(-1)
  t.lexer.skip(1)

lexer = lex.lex()
