from typing import Union, Dict


class Region:
    def __init__(self, item_id: Union[int, str], name: str, code: str, country: Dict[str, str]):
        self.item_id = item_id
        self.name = name
        self.code = code
        self.country = country
        self.country_code = self.country['code']
        self.country_name = self.country['name']
