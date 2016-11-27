from abc import abstractmethod, ABCMeta

class Expression:
    """
    Base class for all mathematical Expressions.
    Combiner operators such as + and * are
    implemented here.
    ``Expression`` and all subclasses are immutable
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, val):
        pass

    def __hash__(self):
        return hash(self.__str__())

    @staticmethod
    def _val_of_exp(exp, val):
        if isinstance(exp, int):
            return exp

        return exp(val)

    @abstractmethod
    def __eq__(self, other):
        pass

    def __ne__(self, other):
        return not self.__eq__(other)

    @abstractmethod
    def degree(self):
        pass

    @staticmethod
    def _calc_degree(exp):
        if isinstance(exp, int):
            return 0

        return exp.degree()

    @abstractmethod
    def __str__(self):
        pass

    def __mul__(self, other):
        from .algebra import Product, Sum
        from .exponent import Exponent

        if other == 1:
            return x

        if self == other:
            """ If both expressions are identical return the square. """
            return Exponent(self, 2)

        if isinstance(other, Product) or isinstance(other, Exponent) or isinstance(other, Sum):
            return other * self

        return Product(self, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power, modulo=None):
        from .exponent import Exponent

        return Exponent(self, power)

    def __rpow__(self, other):
        from  .exponent import Exponent

        return Exponent(other, self)

    def __add__(self, other):
        from .algebra import Sum

        if self == other:
            return 2 * self

        return Sum(self, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        from .algebra import Difference

        if self == other:
            return 0

        return Difference(self, other)

class Identity(Expression):
    def __call__(self, val):
        return val

    def __eq__(self, other):
        return isinstance(other, Identity)

    def degree(self):
        return 1

    def __str__(self):
        return "x"

class Negation(Expression):
    def __init__(self, expr):
        self._expr = expr

    @property
    def expr(self):
        return self._expr

    def __call__(self, val):
        return - self._val_of_exp(self._expr, val)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._expr == other.expr

    def degree(self):
        return self._calc_degree(self._expr)

    def __str__(self):
        return "-" + str(self._expr)

x = Identity()
