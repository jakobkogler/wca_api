from collections import namedtuple
from copy import copy
from wca_api.conditions import Condition


class Table:
    """Collection of rows of a table.
    Supports easy filtering and sorting."""

    def __init__(self, rows: list):
        """Copy rows."""
        self._rows = copy(rows)

    def __getitem__(self, pos):
        """Returns the row at position."""
        return self._rows[pos]

    def __len__(self):
        """Returns the number of rows."""
        return len(self._rows)

    def __str__(self, many=10):
        """Returns a string representation of the first few (default=10) rows."""
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

    def all_to_string(self):
        """Returns a string representation of all rows."""
        return self.__str__(-1)

    def filter(self, condition: Condition):
        """Filter for rows, that satisfy a condition."""
        self._rows = [row for row in self._rows if condition(row)]

    def sort(self, fields, reverse=False):
        """Sort rows by field names."""
        if not isinstance(fields, list):
            fields = [fields]

        self._rows.sort(key=lambda row: tuple(getattr(row, name, None) for name in fields),
                        reverse=reverse)

    def restrict_fields(self, fields):
        """Restrict the columns to the ones defined in fields."""
        if self._rows:
            fields = [field for field in fields if getattr(self._rows[0], field, None) is not None]
        row_type = namedtuple('Row', fields)
        self._rows = [row_type(*(getattr(row, field) for field in fields)) for row in self._rows]

    def top(self, num):
        """Remove every row except the first num ones."""
        self._rows = self._rows[:num]

    def __eq__(self, other):
        """Test equallity."""
        if len(self) != len(other):
            return False
        return all(self[i] == other[i] for i in range(len(self)))
