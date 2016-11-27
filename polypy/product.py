from .commutative import Commutative

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
