from collections import namedtuple
from wca_api.conditions import Condition


class Table:
    """Collection of rows of a table.
    Supports easy filtering and sorting."""

    def __init__(self, rows: list):
        self._rows = rows

    def __getitem__(self, item):
        return self._rows[item]

    def __len__(self):
        return len(self._rows)

    def __str__(self, many=10):
        if self._rows:
            lengths = [len(item) for item in self._rows[0]._fields]
            for index, row in enumerate(self._rows):
                if index == many:
                    break
                lengths = [max(a, b) for a, b in zip(lengths, [len(str(item)) for item in row])]

            row_format = ' | '.join('{{:>{}}}' for _ in self._rows[0]).format(*lengths)
            output = [row_format.format(*self._rows[0]._fields)]
            output.append('-+-'.join('-'*length for length in lengths))
            for index, row in enumerate(self._rows):
                if index == many:
                    break
                output.append(row_format.format(*row))

            return '\n'.join(output)
        else:
            return ''

    def print_all(self):
        print(self.__str__(-1))

    def filter(self, condition: Condition):
        self._rows = [row for row in self._rows if condition(row)]

    def sort(self, by, reverse=False):
        if not isinstance(by, list):
            by = [by]

        self._rows.sort(key=lambda row: tuple(getattr(row, name) for name in by), reverse=reverse)

    def restrict_fields(self, fields):
        Type = namedtuple('Row', fields)
        self._rows = [Type(*(getattr(row, field) for field in fields)) for row in self._rows]

    def top(self, num):
        self._rows = self._rows[:num]

    def __eq__(self, other):
        return self._rows == other._rows
