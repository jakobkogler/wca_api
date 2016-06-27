"""A collection of classes, which can check table rows for conditions."""


class Condition:
    """Base class for all condition checks."""
    pass


class OneOf(Condition):
    """Class for checking, if a certain field in part of a list of items."""

    def __init__(self, field, lst):
        """Store field name and list of items in object."""
        self._field = field
        self._lst = lst

    def __call__(self, compare):
        """Check, if the item compare holds the object condition."""
        return getattr(compare, self._field) in self._lst


class Equal(OneOf):
    """Class for checking, if a certain field is equal to a value."""

    def __init__(self, field, equal):
        super().__init__(field, [equal])


class DNF(Condition):
    """Class for checking, if a certain field is / is not a DNF."""

    def __init__(self, field, dnf=True):
        """Store field name and list of items in object."""
        self._field = field
        self._dnf = dnf

    def __call__(self, compare):
        """Check, if the item compare holds the object condition."""
        return (getattr(compare, self._field) != -1) == self._dnf
