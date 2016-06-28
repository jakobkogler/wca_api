import pytest
from wca_api.table import Table
from wca_api.conditions import Equal, OneOf, DNF, TimeBetterThan
from collections import namedtuple


class TestConditions:
    row_type = namedtuple('Row', 'name country best')

    alice_deu_957 = row_type('Alice', 'Germany', 957)
    bob_aut_1138 = row_type('Bob', 'Austria', 1138)
    bob_aut_999 = row_type('Bob', 'Austria', 999)
    carol_deu_1527 = row_type('Carol', 'Germany', 1527)
    dave_fra_999 = row_type('Dave', 'France', 999)
    eve_fra_dnf = row_type('Eve', 'France', -1)

    def test_sort(self):
        lst = [self.alice_deu_957, self.bob_aut_1138, self.bob_aut_999, self.carol_deu_1527, self.dave_fra_999]

        # sort by country
        table = Table(lst)
        table.sort('country')
        assert table == Table([self.bob_aut_1138, self.bob_aut_999, self.dave_fra_999, self.alice_deu_957, self.carol_deu_1527])

        # sort by country reverse
        table = Table(lst)
        table.sort('country', reverse=True)
        assert table == Table([self.alice_deu_957, self.carol_deu_1527, self.dave_fra_999, self.bob_aut_1138, self.bob_aut_999])

        # sort by int value
        table = Table(lst)
        table.sort('best')
        assert table == Table([self.alice_deu_957, self.bob_aut_999, self.dave_fra_999, self.bob_aut_1138, self.carol_deu_1527])

        # sort by int value reverse
        table = Table(lst)
        table.sort('best', reverse=True)
        assert table == Table([self.carol_deu_1527, self.bob_aut_1138, self.bob_aut_999, self.dave_fra_999, self.alice_deu_957])

        # sort by unknown field name
        table = Table(lst)
        table.sort('average')
        assert table == Table(lst)

    def test_restrict_fields(self):
        lst = [self.alice_deu_957, self.bob_aut_999]

        # restrict to name
        row_type = namedtuple('Row', 'name')
        lst2 = [row_type('Alice'), row_type('Bob')]
        table = Table(lst)
        table.restrict_fields(['name'])
        assert table == Table(lst2)

        # restrict to best and name
        row_type = namedtuple('Row', 'best name')
        lst2 = [row_type(957, 'Alice'), row_type(999, 'Bob')]
        table = Table(lst)
        table.restrict_fields(['best', 'name'])
        assert table == Table(lst2)

        # restrict to unknown name
        row_type = namedtuple('Row', 'name')
        lst2 = [row_type('Alice'), row_type('Bob')]
        table = Table(lst)
        table.restrict_fields(['name', 'average'])
        assert table == Table(lst2)
