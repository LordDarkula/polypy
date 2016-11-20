from abc import ABCMeta, abstractmethod

from .base import Expression


class Commutative(Expression):
    """
    Base class for all commutative expressions
    such as ``Product`` and ``Sum``.
    """
    __metaclass__ = ABCMeta

    def __init__(self, *args):
        self._exprs = set()
        for arg in args:
            self.exprs.add(arg)

    @property
    def exprs(self):
        return self._exprs

    def __eq__(self, other):
        return self._exprs == other.exprs

    @abstractmethod
    def __call__(self, val):
        pass


class Product(Commutative):
    def __init__(self, *args):
        super(Product, self).__init__(args)

    def __call__(self, val):
        prod = 1
        for expr in self._exprs:
            prod *= expr

        return prod

    def degree(self):
        deg = 0
        for expr in self._exprs:
            deg += self._calc_degree(expr)

        return deg

    def order(self):
        ordered = [expr for expr in self._exprs]
        ordered.sort(key=lambda x: self._calc_degree(x), reverse=True)
        return ordered


    def __str__(self):
        return ''.join("{} + ".format(expr) for expr in self.order())[:-2]

    def __mul__(self, other):
        if other == self.expr1:
            return other * self.expr1 * self.expr2

        if other == self.expr2:
            return other * self.expr2 * self.expr1

        if isinstance(other, Product):
            """ If other is a Product and one of it's terms matches this Expression,
            redistribute to multiply that term with this one first. """
            if self.expr1 == other.expr1:
                return self.expr2 * other.expr2 * self.expr1**2

            if self.expr2 == other.expr2:
                return self.expr1 * other.expr1 * self.expr2**2

            if self.expr1 == other.expr2:
                return self.expr2 * other.expr1 * self.expr1**2

            if self.expr2 == other.expr1:
                return self.expr1 * other.expr2 * self.expr2**2

        return Product(self, other)

    def __pow__(self, power, modulo=None):
        return self.expr1**power * self.expr2**power

class Sum(Commutative):
    def __init__(self, expr1, expr2):
        super(Sum, self).__init__(expr1, expr2)

    def __call__(self, val):
        return self._val_of_exp(self.expr1, val) \
               + self._val_of_exp(self.expr2, val)

    def degree(self):
        return max(self._calc_degree(self.expr1), self._calc_degree(self.expr2))

    def __str__(self):
        if self._calc_degree(self.expr2) > self._calc_degree(self.expr1):
            return str(self.expr2) + " + " + str(self.expr1)

        return str(self.expr1) + " + " + str(self.expr2)

    def __mul__(self, other):
        return self.expr1 * other + self.expr2 * other

class Difference(Expression):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def __call__(self, val):
        return self._val_of_exp(self.expr1, val) \
               - self._val_of_exp(self.expr2, val)

    def degree(self):
        return max(self._calc_degree(self.expr1), self._calc_degree(self.expr2))

    def __str__(self):
        if self._calc_degree(self.expr2) > self._calc_degree(self.expr1):
            return str(self.expr2) + " - " + str(self.expr1)

        return str(self.expr1) + " - " + str(self.expr2)

    def __mul__(self, other):
        return self.expr1 * other - self.expr2 * other
