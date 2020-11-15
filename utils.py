from typing import List

from requests import get, Response

from entities import Region


def get_data(**params) -> Response:
    param_substring = ''
    for param in params:
        param_substring = param_substring + f'&{param}={params[param]}'
    url = f'https://regions-test.2gis.com/1.0/regions?{param_substring}'
    return get(url)


def get_regions(request) -> List:
    regions = []
    if request:
        regions = [Region(item_id=item['id'],
                          name=item['name'],
                          code=item['code'],
                          country=item['country']) for item in request]
    return regions
