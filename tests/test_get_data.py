import pytest
from get_data import GetData


def test_get_pollution_data():
    assert GetData.get_pollution_data(2, 2018) == 'hhjfgsd'


