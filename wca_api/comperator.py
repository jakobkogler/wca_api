class Comperator:
    pass


class OneOf(Comperator):
    def __init__(self, field, lst):
        self._field = field
        self._lst = lst

    def __call__(self, compare):
        return getattr(compare, self._field) in self._lst


class Equal(OneOf):
    def __init__(self, field, equal):
        super().__init__(field, [equal])
