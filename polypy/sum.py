from .commutative import Commutative

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

