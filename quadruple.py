from datastructures import *

class Quadruple(object):
    """ Quadruple class

    One quadruple, which has operator, left operand, right operand and result.
    """
    def __init__(self):
        self.id = -1
        self.operator = None
        self.left = None
        self.right = None
        self.result = None

    def build(self, operator, left, right, result):
        """Build Quadruple

        Generates one cuadruple
        """
        self.operator = operator
        self.left = left
        self.right = right
        self.result = result

    def print(self):
        """Print Quadruple

        Prints all arguments in quadruple
        """
        op = quadruple_operations.index(self.operator)
        return [op, self.left, self.right, self.result]

class QuadrupleList(object):
    """ Quadruple LIst

    Contains all quadruples"""
    quadruple_list = []
    jump_stack = zStack()
    next_quadruple = 0

    @classmethod
    def push(self, quad):
        """Push Quadruple

        Push a Quadruple to the list"""
        quad.id = self.next_quadruple
        next_quadruple += 1
        quadruple_list.append(quad)

