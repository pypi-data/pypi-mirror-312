from ibis.selectors import all as iall, across

from ibis import _


class all(object):
    def __init__(self):
        self.selector = iall()

    def __rmul__(self, other):
        return across(iall(), _ * other)

    def __mul__(self, other):
        return across(iall(), _ * other)
