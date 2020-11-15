import allure
import pytest

from utils import get_data, get_regions


@allure.epic('API')
@allure.feature('Regions API')
class TestSuiteRegionsApi:

    @allure.story('Фильтрация по названию региона')
    @pytest.mark.usefixtures('get_regions_list')
    @pytest.mark.parametrize('params, expect_regions', [({'q': 'новосибирск'}, ['Новосибирск']),
                                                        ({'q': 'ск'}, []),
                                                        ({'q': 'ноя'}, ['Красноярск']),
                                                        ({'q': 'Novosibirsk'}, []),
                                                        ({'q': 'ТОМСК', 'country_code': 'kz'}, ['Томск'])])
    def test_regions_name_filter(self, params, expect_regions, get_regions_list):
        with allure.step(f'Список полученных регионов соответствует [{expect_regions}]'):
            regions_names = [region.name for region in get_regions_list]
            assert len(get_regions_list) == len(expect_regions)
            assert set(expect_regions) == set(regions_names)

    @allure.story('Фильтрация по country_code')
    @pytest.mark.usefixtures('get_regions_list')
    @pytest.mark.parametrize('params, exp_country_code', [({'country_code': 'ru'}, 'ru'),
                                                          ({'country_code': 'kz'}, 'kz'),
                                                          ({'country_code': 'kg'}, 'kg'),
                                                          ({'country_code': 'cz'}, 'cz')])
    def test_country_code_filter(self, params, exp_country_code, get_regions_list):
        with allure.step(f'Все регионы из списка соответствуют country_code: {exp_country_code}'):
            for region in get_regions_list:
                assert region.country_code == exp_country_code

    @allure.story('Изменение страницы с результатами')
    @pytest.mark.usefixtures('get_response')
    @pytest.mark.parametrize('params', [{'page': 2}, {'page': 10}, {'page': 0}])
    def test_pagination(self, params, get_response):
        if params['page'] > 0:
            with allure.step(f'Получить списки названий регионов '):
                _first_page_items = get_data(page=1, page_size=15).json().get('items')
                first_regions_names = set([region.name for region in get_regions(_first_page_items)])
                other_page_items = get_response.json().get('items')
                other_regions_names = set([region.name for region in get_regions(other_page_items)])
            with allure.step(f'Список регионов первой и {params["page"]} страницы отличны'):
                assert not first_regions_names == other_regions_names
        else:
            with allure.step('Запрос не обработан сервером'):
                assert get_response.status_code == 500

    @allure.story('Изменение количества выдаваемых на странице результатов')
    @pytest.mark.usefixtures('get_response_json')
    @pytest.mark.parametrize('params, items_count', [({'page_size': 0}, None),
                                                     ({'page_size': 4}, None),
                                                     ({'page_size': 5}, 5),
                                                     ({'page_size': 6}, None),
                                                     ({'page_size': 10}, 10),
                                                     ({'page_size': 11}, None),
                                                     ({'page_size': 16}, None)])
    def test_page_sizing(self, params, items_count, get_response_json):
        if params['page_size'] not in [5, 10, 15]:
            with allure.step('Сервер возвратил ошибку'):
                assert get_response_json.get('error')['message'] == \
                       "Параметр 'page_size' может быть одним из следующих значений: 5, 10, 15"
        else:
            with allure.step(f'Получить список регионов '):
                regions = get_response_json.get('items')
            with allure.step(f'Количество регионов соответствует {items_count}'):
                assert len(regions) == items_count


@allure.epic('API')
@allure.feature('Regions API')
@pytest.mark.usefixtures('get_regions_list_class')
@pytest.mark.parametrize('params', [{}], scope='class')
class TestSuiteRegionsApiDefault:

    @allure.story('Количество возвращаемых по умолчанию регионов')
    def test_default_page_size(self, get_regions_list_class, page_size=15):
        with allure.step(f'Количество регионов на странице соответствует {page_size}'):
            assert len(get_regions_list_class) == page_size

    @allure.story('Возвращаемый по умолчанию номер страницы')
    def test_default_page_number(self, get_regions_list_class, page=1):
        with allure.step('Получить списки названий регионов'):
            default_regions_names = set([region.name for region in get_regions_list_class])
            _response_page_items = get_data(page=page).json().get('items')
            response_regions_names = set([region.name for region in get_regions(_response_page_items)])
        with allure.step(f'Номер страницы соответствует {page}'):
            assert default_regions_names == response_regions_names

    @allure.story('Возвращаемый по умолчанию country_code у регионов')
    def test_default_country_code(self, get_regions_list_class):
        with allure.step('Регионы имеют различный country_code'):
            assert len(set(region.country_code for region in get_regions_list_class)) > 1
