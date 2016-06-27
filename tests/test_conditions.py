import pytest
from wca_api.table import Table
from wca_api.conditions import Equal
from collections import namedtuple


class TestConditions:
    row_type = namedtuple('Row', 'name country best')

    alice_deu_957 = row_type('Alice', 'Germany', 957)
    bob_aut_1138 = row_type('Bob', 'Austria', 1138)
    bob_aut_999 = row_type('Bob', 'Austria', 999)
    carol_deu_1527 = row_type('Carol', 'Germany', 1527)
    dave_fra_999 = row_type('Dave', 'France', 999)

    def test_equal(self):
        lst = [self.alice_deu_957, self.bob_aut_1138, self.bob_aut_999, self.carol_deu_1527, self.dave_fra_999]

        # filter by name
        table = Table(lst)
        table.filter(Equal('name', 'Bob'))
        assert table == Table([self.bob_aut_1138, self.bob_aut_999])
        table.filter(Equal('name', 'Alice'))
        assert table == Table([])

        # filter by country
        table = Table(lst)
        table.filter(Equal('country', 'Germany'))
        assert table == Table([self.alice_deu_957, self.carol_deu_1527])

        # filter by time
        table = Table(lst)
        table.filter(Equal('best', 999))
        assert table == Table([self.bob_aut_999, self.dave_fra_999])

        # filter by unknown item
        table = Table(lst)
        table.filter(Equal('name', 'Eve'))
        assert table == Table([])

        # filter by unknown field
        table = Table(lst)
        table.filter(Equal('average', 1000))
        assert table == Table([])
