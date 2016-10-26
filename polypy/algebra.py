from .base import Expression


class Identity(Expression):
    def __call__(self, val):
        return val

    def degree(self):
        return 1

    def __str__(self):
        return "x"

x = Identity()

class Multiplier(Expression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

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

class Adder(Expression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def __call__(self, val):
        return self._val_of_exp(self.exp1, val) \
               + self._val_of_exp(self.exp2, val)

    def degree(self):
        max(self._calc_degree(self.exp1), self._calc_degree(self.exp2))
