from .commutative import Commutative

class Product(Commutative):
    def __init__(self, *args):
        super(Product, self).__init__(*self.simplified(*args))

    def simplified(self, *args):
        """
        Returns a sequence containing expressions that make a simplified Product.
        Used when ``Product`` is initialized to simplify.
        Uses ``self.exprs`` when no arguments are provided.

        :type: args: int or Commutative
        :rtype: seq
        """
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

    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            return Product(*self._exprs, other)

        no_overlap = self._exprs.union(other.exprs) - self._exprs.intersection(other.exprs)
        overlap = set([expr**2 for expr in self._exprs.intersection(other.exprs)])

        return no_overlap.union(overlap)

    def __pow__(self, power, modulo=None):
        return Product(frozenset([expr**power for expr in self._exprs]))
