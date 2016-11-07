# -*- coding: utf-8 -*-
# Data structures used for semantic analysis

# Variables dictionary with scope
variables = {
  'global' : {
  },
  'main' : {
   },
  'function' : {
  },
  'constants' : {
  }
}

# Functions dictionary
functions = {}

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

current_function = {
  'id' : None,
  'type' : None
}

operators = {
 '+'  = 1,
 '-'  = 2,
 '*'  = 3,
 '/'  = 4,
 '%'  = 5,
 '='  = 6,
 '==' = 7,
 '>'  = 8,
 '<'  = 9,
 '<=' = 10,
 '>=' = 11,
 '<>' = 12,
 '&&' = 13,
 '||' = 14
}