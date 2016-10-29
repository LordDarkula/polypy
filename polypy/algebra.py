from abc import ABCMeta

from .base import Expression
from .exponent import Exponent

class Commutative(Expression):

    __metaclass__ = ABCMeta

    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def __eq__(self, other):
        return isinstance(other, self) and \
               (self.exp1 == other.exp1 and self.exp2 == other.exp2) or \
               (self.exp1 == other.exp2 and self.exp2 == other.exp1)


class Product(Commutative):
    def __init__(self, exp1, exp2):
        super(Product, self).__init__(exp1, exp2)

    def __call__(self, val):
        return self._val_of_exp(self.exp1, val) \
               * self._val_of_exp(self.exp2, val)

    def degree(self):
        return self._calc_degree(self.exp1) \
               + self._calc_degree(self.exp2)

    def __str__(self):
        if self._calc_degree(self.exp2) < self._calc_degree(self.exp1):
            return str(self.exp2) + str(self.exp1)

        return str(self.exp1) + str(self.exp2)

    def __mul__(self, other):
        if isinstance(other, Product):
            """ If other is a Product and one of it's terms matches this Expression,
            redistribute to multiply that term with this one first. """
            if self == other.exp1:
                return self._redistribute(other.exp1, other.exp2)

            if self == other.exp2:
                return self._redistribute(other.exp2, other.exp1)

            return super(Product, self).__mul__(other)

    def _redistribute(self, identical_exp, other_exp):
        return (identical_exp * self) * other_exp

    def __pow__(self, power, modulo=None):
        return self.exp1**power + self.exp2**power

class Sum(Commutative):
    def __init__(self, exp1, exp2):
        super(Sum, self).__init__(exp1, exp2)

    def __call__(self, val):
        return self._val_of_exp(self.exp1, val) \
               + self._val_of_exp(self.exp2, val)

    def degree(self):
        return max(self._calc_degree(self.exp1), self._calc_degree(self.exp2))

    def __str__(self):
        if self._calc_degree(self.exp2) > self._calc_degree(self.exp1):
            return str(self.exp2) + " + " + str(self.exp1)

        return str(self.exp1) + " + " + str(self.exp2)

    def __mul__(self, other):
        return self.exp1 * other + self.exp2 * other
