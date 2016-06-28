import pytest
from collections import namedtuple
from wca_api.conditions import Equal, OneOf, DNF, TimeBetterThan
from wca_api.table import Table


class TestConditions:
    row_type = namedtuple('Row', 'name country best')

    alice_deu_957 = row_type('Alice', 'Germany', 957)
    bob_aut_1138 = row_type('Bob', 'Austria', 1138)
    bob_aut_999 = row_type('Bob', 'Austria', 999)
    carol_deu_1527 = row_type('Carol', 'Germany', 1527)
    dave_fra_999 = row_type('Dave', 'France', 999)
    eve_fra_dnf = row_type('Eve', 'France', -1)

    def test_equal(self):
        lst = [self.alice_deu_957, self.bob_aut_1138, self.bob_aut_999,
               self.carol_deu_1527, self.dave_fra_999]

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

    def test_oneof(self):
        lst = [self.alice_deu_957, self.bob_aut_1138, self.bob_aut_999,
               self.carol_deu_1527, self.dave_fra_999]

        # filter by name
        table = Table(lst)
        table.filter(OneOf('name', ['Bob']))
        assert table == Table([self.bob_aut_1138, self.bob_aut_999])

        # filter by countries
        table = Table(lst)
        table.filter(OneOf('country', ['France', 'Germany']))
        assert table == Table([self.alice_deu_957, self.carol_deu_1527, self.dave_fra_999])

        # filter by nothing
        table = Table(lst)
        table.filter(OneOf('country', []))
        assert table == Table([])

        # filter by all countries
        table = Table(lst)
        table.filter(OneOf('country', ['Austria', 'Germany', 'France']))
        assert table == Table(lst)

        # filter by unknown field
        table = Table(lst)
        table.filter(OneOf('average', [999]))
        assert table == Table([])

        # filter by time
        table = Table(lst)
        table.filter(OneOf('best', [999, 1527]))
        assert table == Table([self.bob_aut_999, self.carol_deu_1527, self.dave_fra_999])

    def test_dnf(self):
        lst = [self.alice_deu_957, self.dave_fra_999, self.eve_fra_dnf]

        # filter all dnfs
        table = Table(lst)
        table.filter(DNF('best'))
        assert table == Table([self.eve_fra_dnf])

        # filter all non-dnfs
        table = Table(lst)
        table.filter(DNF('best', dnf=False))
        assert table == Table([self.alice_deu_957, self.dave_fra_999])

        # filter by unknown field
        table = Table(lst)
        table.filter(DNF('average'))
        assert table == Table([])

        # filter by unknwon field for non-dnfs
        table = Table(lst)
        table.filter(DNF('average', dnf=False))
        assert table == Table(lst)

        # filter by string field
        table = Table(lst)
        table.filter(DNF('country'))
        assert table == Table([])

        # filter by string field for non-dnfs
        table = Table(lst)
        table.filter(DNF('country', dnf=False))
        assert table == Table(lst)

    def test_time_better_than(self):
        lst = [self.alice_deu_957, self.bob_aut_1138, self.bob_aut_999,
               self.carol_deu_1527, self.dave_fra_999]

        # filter for times smaller than 1000
        table = Table(lst)
        table.filter(TimeBetterThan('best', 1000))
        assert table == Table([self.alice_deu_957, self.bob_aut_999, self.dave_fra_999])

        # filter for times smaller than 500
        table = Table(lst)
        table.filter(TimeBetterThan('best', 500))
        assert table == Table([])

        # filter by unknown field
        table = Table(lst)
        table.filter(TimeBetterThan('average', 1000))
        assert table == Table([])

        # filter by string field
        table = Table(lst)
        table.filter(TimeBetterThan('country', 1000))
        assert table == Table([])
