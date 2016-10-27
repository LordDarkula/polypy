from .base import Expression


class Product(Expression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    # TODO Override __mul__ and check if signature of any exp matches other and return approppriate exponent
    def __call__(self, val):
        return self._val_of_exp(self.exp1, val) \
               * self._val_of_exp(self.exp2, val)

    def __eq__(self, other):
        if isinstance(other, Product):
            if self.exp1 == other.exp1 or self.exp2 == other.exp2:
                return True

            if self.exp1 == other.exp2 or self.exp2 == other.exp1:
                return True

        return False

    def degree(self):
        return self._calc_degree(self.exp1) \
               + self._calc_degree(self.exp2)

    def __str__(self):
        if self._calc_degree(self.exp2) < self._calc_degree(self.exp1):
            return str(self.exp2) + str(self.exp1)

        return str(self.exp1) + str(self.exp2)

class Exponent(Expression):
    def __init__(self, base, exponent):
        self.base = base
        self.exponent = exponent

    def __call__(self, val):
        return self._val_of_exp(self.base, val) \
               ** self._val_of_exp(self.exponent, val)

    def __eq__(self, other):
        return isinstance(other, Exponent) \
               and self.base == other.base \
               and self.exponent == other.exponent

    def degree(self):
        if isinstance(self.exponent, int):
            return self.exponent

        return 100

    def __str__(self):
        return str(self.base) + "^" + str(self.exponent)

class Sum(Expression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def __call__(self, val):
        return self._val_of_exp(self.exp1, val) \
               + self._val_of_exp(self.exp2, val)

    def __eq__(self, other):
        if isinstance(other, Product):
            if self.exp1 == other.exp1 or self.exp2 == other.exp2:
                return True

            if self.exp1 == other.exp2 or self.exp2 == other.exp1:
                return True

        return False

    def degree(self):
        return max(self._calc_degree(self.exp1), self._calc_degree(self.exp2))

    def __str__(self):
        if self._calc_degree(self.exp2) > self._calc_degree(self.exp1):
            return str(self.exp2) + " + " + str(self.exp1)

        return str(self.exp1) + " + " + str(self.exp2)
