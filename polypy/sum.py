from .commutative import Commutative

class Sum(Commutative):
    def __init__(self, *args):
        super(Sum, self).__init__(*args)

    def simplified(self, *args):
        """
        Returns a sequence containing expressions that make a simplified Sum.
        Used when ``Sum`` is initialized to simplify.
        Uses ``self.exprs`` when no arguments are provided.

        :type: args: int or Expression
        :rtype: seq
        """
        constant = 0
        args = args or self._exprs

        for arg in args:
            if isinstance(arg, int):
                # 0 can be eliminated because x + 0 = 0
                if arg == 0:
                    continue

                constant += arg
            else:
                yield arg

            if constant != 0:
                yield constant

    def __call__(self, val):
        sum = 0
        for expr in self._exprs:
            sum += self._val_of_exp(expr, val)

        return sum

    def degree(self):
        """
        Returns degree of the sum which is the degree of the highest
        degree term.

        :rtype: int
        """
        return max(*[self._calc_degree(expr) for expr in self._exprs])

    def order(self, ascending=True):
        """
        Converts ''frozenset'' exprs into ''list'' ordered by degree.
        :rtype: list
        """
        return super(Sum, self).order(ascending=False)

    def __str__(self):
        return ''.join("{} + ".format(expr) for expr in self.order())[:-2]  # Removes leftover +

    def __mul__(self, other):
        return Sum(*[expr * other for expr in self._exprs])

