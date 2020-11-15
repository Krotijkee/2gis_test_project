import pytest

from utils import get_data, get_regions


@pytest.fixture(scope='function')
def get_response(params):
    yield get_data() if len(params) == 0 else get_data(**params)


@pytest.fixture(scope='function')
def get_response_json(get_response):
    yield get_response.json()


@pytest.fixture(scope='function')
def get_regions_list(get_response):
    yield get_regions(get_response.json().get('items'))


@pytest.fixture(scope='class')
def get_response_class(params):
    yield get_data() if len(params) == 0 else get_data(**params)


@pytest.fixture(scope='class')
def get_regions_list_class(get_response_class):
    yield get_regions(get_response_class.json().get('items'))

