import pytest
from data_fetcher.get_data import GetData

def test_setting_name():
    hackney = GetData('hackney')
    assert hackney.authority_name == 'Hackney'

