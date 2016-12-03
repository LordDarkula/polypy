from .commutative import Commutative
from .exponent import Exponent

class Product(Commutative):
    def __init__(self, *args):
        super(Product, self).__init__(*self.simplified(*args))

    def simplified(self, *args):
        coefficient = 1
        args = args or self._exprs

        for arg in args:
            if isinstance(arg, int):
                # If any part is 0 the whole thing is 0
                if arg == 0:
                    yield None
                # 1 can be eliminated because 1 * x = x
                if arg == 1:
                    continue

                coefficient *= arg
            else:
                yield arg

            yield coefficient

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
        return super(Product, self).order(ascending=True)

    def same_base(self, other):
        return isinstance(other, self.__class__) and \
               self.rem_int() == other.rem_int()

    def rem_int(self):
        return frozenset([expr for expr in self._exprs if not isinstance(expr, int)])

    def __str__(self):
        return ''.join("{} * ".format(expr) for expr in self.order())[:-2] # Removes leftover *

    def _combine_exp(self):
        full_set = set(self._exprs)
        temp_set = set()
        for expr in full_set:
            if isinstance(expr, Exponent):

                for poss_exp in full_set:
                    if expr.base == poss_exp or isinstance(poss_exp, Exponent):
                        temp_set.add(expr.__mul__(poss_exp))
                        full_set.remove(expr)
                        full_set.remove(poss_exp)
                        break
                else:
                    temp_set.add(expr)

            else:
                temp_set.add(expr)

        self._exprs = frozenset(temp_set)

    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            return Product(*self._exprs, other)

        no_overlap = self._exprs.union(other.exprs) - self._exprs.intersection(other.exprs)
        overlap = set([expr**2 for expr in self._exprs.intersection(other.exprs)])

        return no_overlap.union(overlap)

    def __pow__(self, power, modulo=None):
        return Product(frozenset([expr**power for expr in self._exprs]))
