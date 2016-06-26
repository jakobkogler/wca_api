from collections import namedtuple


class table:
    """Collection of rows of a table.
    Supports easy filtering and sorting."""

    def __init__(self, rows: list):
        self._name = type(rows[0]).__name__ if rows else ''
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
                lengths = [max(a, b) for a, b in zip(lengths, map(len, row))]

            row_format = ' '.join('{{:>{}}}' for _ in self._rows[0]).format(*lengths)
            output = [row_format.format(*self._rows[0]._fields)]
            for index, row in enumerate(self._rows):
                if index == many:
                    break
                output.append(row_format.format(*row))

            return '\n'.join(output)
        else:
            return ''

    def print_all(self):
        print(self.__str__(-1))

    def filter(self, conditions: dict):
        if self._rows:
            fields = self._rows[0]._fields
            conditions = {field: allowed if isinstance(allowed, list) else [allowed]
                          for field, allowed in conditions.items() if field in fields}
            self._rows = [row for row in self._rows
                          if all(getattr(row, field) in allowed for field, allowed in conditions.items())]

    def sort(self, by, reverse=False):
        if not isinstance(by, list):
            by = [by]

        if self._rows:
            fields = self._rows[0]._fields
            by = [name for name in by if name in fields]

            self._rows.sort(key=lambda row: tuple(getattr(row, name) for name in by), reverse=reverse)

    def restrict_fields(self, fields):
        name = ''
        if self._rows:
            fields = [field for field in fields if field in self._rows[0]._fields]

        Type = namedtuple(self._name, fields)
        self._rows = [Type(*(getattr(row, field) for field in fields)) for row in self._rows]

    def top(self, num):
        self._rows = self._rows[:num]