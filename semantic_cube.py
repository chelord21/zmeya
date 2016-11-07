# Semantic cube
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
