import math

from .base import Expression


class Sine(Expression):
    def __init__(self, exp):
        self.exp = exp

    def __call__(self, val):
        return math.sin(self._val_of_exp(self.exp, val))

    def __eq__(self, other):
        return isinstance(other, Sine) and self.exp == other.exp

    def degree(self):
        return 1

    def __str__(self):
        return "sin(" + str(self.exp) + ")"
