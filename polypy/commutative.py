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



