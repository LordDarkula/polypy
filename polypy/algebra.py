from abc import ABCMeta, abstractmethod

from .base import Expression


class Commutative(Expression):
    """
    Base class for all commutative expressions
    such as ``Product`` and ``Sum``.
    """
    __metaclass__ = ABCMeta

    def __init__(self, *args):
        self._exprs = frozenset(args)

    @property
    def exprs(self):
        return self._exprs

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self._exprs == other.exprs

    @abstractmethod
    def __call__(self, val):
        pass

    def order(self, ascending=False):
        """
        Converts ''frozenset'' exprs into ''list'' ordered by degree.
        :rtype: list
        """
        ordered = [expr for expr in self._exprs]
        ordered.sort(key=lambda x: self._calc_degree(x), reverse=ascending)
        return ordered


class Product(Commutative):
    def __init__(self, *args):
        super(Product, self).__init__(*args)

        temp_exprs = set()
        coefficient = 1

        for arg in args:
            if isinstance(arg, int):
                # If any part is 0 the whole thing is 0
                if arg == 0:
                    self._exprs = frozenset([0])
                    return
                # 1 can be eliminated because 1 * x = x
                if arg == 1:
                    continue

                # Integer parts are collected and combined to form coefficient
                coefficient *= arg

            else:
                temp_exprs.add(arg)

        if coefficient != 1:
            temp_exprs.add(coefficient)

        self._exprs = frozenset(temp_exprs)

    def __call__(self, val):
        prod = 1
        for expr in self._exprs:
            prod *= self._val_of_exp(expr, val)

        return prod

    def degree(self):
        """
        Returns total degree (ex degree x is 1, degree 3x^3 is 3) of product.
        :rtype: int
        """
        deg = 0
        for expr in self._exprs:
            deg += self._calc_degree(expr)

        return deg

    def order(self, ascending=True):
        """
        Converts ''frozenset'' exprs into ''list'' ordered by degree.
        :rtype: list
        """
        super(Product, self).order(ascending=True)

    def same_base(self, other):
        return isinstance(other, self.__class__) and \
               self.rem_int() == other.rem_int()

    def rem_int(self):
        return frozenset([expr for expr in self._exprs if not isinstance(expr, int)])

    def __str__(self):
        return ''.join("({}) * ".format(expr) for expr in self.order())[:-2] # Removes leftover *

    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            return Product(self._exprs.union(other.exprs))

        no_overlap = self._exprs.union(other.exprs) - self._exprs.intersection(other.exprs)
        overlap = set([expr**2 for expr in self._exprs.intersection(other.exprs)])

        return no_overlap.union(overlap)

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
