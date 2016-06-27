class Condition:
    pass


class OneOf(Condition):
    def __init__(self, field, lst):
        self._field = field
        self._lst = lst

    def __call__(self, compare):
        return getattr(compare, self._field) in self._lst


class Equal(OneOf):
    def __init__(self, field, equal):
        super().__init__(field, [equal])


class DNF(Condition):
    def __init__(self, field, dnf=True):
        self._field = field
        self._dnf = dnf

    def __call__(self, compare):
        return (getattr(compare, self._field) != -1) == self._dnf
