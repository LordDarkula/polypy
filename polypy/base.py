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
        from .algebra import Product, Exponent

        if self == other:
            """ If both expressions are identical return the square. """
            return Exponent(self, 2)

        if isinstance(other, Product) or isinstance(other, Exponent):
            return other * self

        return Product(self, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power, modulo=None):
        from .algebra import Exponent

        return Exponent(self, power)

    def __rpow__(self, other):
        from  .algebra import Exponent

        return Exponent(other, self)

    def __add__(self, other):
        from .algebra import Sum

        return Sum(self, other)

    def __radd__(self, other):
        return self.__add__(other)

class Identity(Expression):
    def __call__(self, val):
        return val

    def __eq__(self, other):
        return isinstance(other, Identity)

    def degree(self):
        return 1

    def __str__(self):
        return "x"

x = Identity()