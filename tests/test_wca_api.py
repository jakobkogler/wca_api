import pytest
from wca_api.wca_api import update_tsv_export, load


def test_load():
    assert update_tsv_export()

    table = load('Persons', 'id')
    assert table[0].id == '1982BORS01'
