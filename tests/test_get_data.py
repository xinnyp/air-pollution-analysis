import pytest
from get_data import GetData


def get_local_authority_data():
    hackney = GetData(authority_name='Hackney')
    assert type(hackney) == str