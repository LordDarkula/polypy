import math

from .base import Expression


class Exponent(Expression):
    def __init__(self, base, exponent):
        self._base = base
        self._exponent = exponent

    @property
    def base(self):
        return self._base

    @property
    def exponent(self):
        return self._exponent

    def __call__(self, val):
        return self._val_of_exp(self._base, val) \
               ** self._val_of_exp(self._exponent, val)

    def __eq__(self, other):
        return isinstance(other, Exponent) \
               and self._base == other.base \
               and self._exponent == other.exponent

    def degree(self):
        if isinstance(self._exponent, int):
            return self._exponent

        return 100

    def __str__(self):
        return str(self._base) + "^" + str(self._exponent)

    def __mul__(self, other):
        if isinstance(other, self.__class__) and self._base == other.base:
            """ If both exponents have the same base """
            return Exponent(self._base, self._exponent + other.exponent)

        if self._base == other:
            """ If other is an Exponent and base matches this Expression,
            return Exponent of same base with +1 exponent."""
            return Exponent(self._base, self._exponent + 1)

        return super(Exponent, self).__mul__(other)

    def __pow__(self, power, modulo=None):
        return Exponent(self.base, self.exponent*power)

class Logarithm(Expression):
    def __init__(self, base, product):
        self.base = base
        self.product = product

    def __call__(self, val):
        return math.log(self._val_of_exp(self.product, val), self._val_of_exp(self.base, val))

    def __eq__(self, other):
        return isinstance(other, Logarithm) \
               and self.base == other.base \
               and self.product == other.product

    def degree(self):
        return 0

    def __str__(self):
        if self.base == 10:
            return "log(" + str(self.product) + ")"

        if self.base == math.e:
            return "ln(" + str(self.product) + ")"

        return "log<base: " + str(self.base) + " >(" + str(self.product) + ")"

def log(val):
    return Logarithm(10, val)

def ln(val):
    return Logarithm(math.e, val)