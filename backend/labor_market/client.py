import logging
import requests
from dacite import Config, from_dict
from labor_market.dto import VacancyFull, VacancyList
log = logging.getLogger(__name__)


class HhRuRequestError(Exception):
    def __init__(self, code: int = None, message: str = None) -> None:
        super().__init__(self, f'hh.ru request error, code: {code}, message: {message}')


class HhRuApiClient:
    _dacite_config: Config = Config(check_types=False)
    _base_url: str = 'https://api.hh.ru'
    _vacancies_url: str = 'vacancies'
    _true_string: str = 'true'
    _search_query_param: str = 'text'
    _premium_query_param: str = 'premium'
    _page_query_param: str = 'page'
    _page_size_query_param: str = 'per_page'

    @classmethod
    def get_vacancy_by_id(cls, vacancy_id: int) -> VacancyFull:
        url = f'{cls._base_url}/{cls._vacancies_url}/{vacancy_id}'
        response = requests.get(url=url)

        if response.status_code == 404:
            raise VacancyFull.WasNotFound(response.status_code, response.text)

        if response.status_code != 200:
            log.error(f'Cannot get vacancy with id: {vacancy_id}')
            raise HhRuRequestError(response.status_code, response.text)

        vacancy_data: dict = response.json()
        vacancy: VacancyFull = \
            from_dict(data_class=VacancyFull, data=vacancy_data, config=cls._dacite_config)

        return vacancy

    @classmethod
    def find_vacancies(cls, key_words: str, page: int, page_size: int) -> VacancyList:
        url = f'{cls._base_url}/{cls._vacancies_url}'
        params = {
            cls._search_query_param: key_words,
            cls._premium_query_param: cls._true_string,
            cls._page_query_param: page,
            cls._page_size_query_param: page_size
        }
        response = requests.get(url=url, params=params)

        if response.status_code == 404:
            return VacancyList.empty()

        if response.status_code != 200:
            log.error(f'Cannot find vacancies by key words: {key_words}, page: {page}, page_size: {page_size}')
            raise HhRuRequestError(response.status_code, response.text)

        vacancy_list_data: dict = response.json()
        vacancy_list: VacancyList = \
            from_dict(data_class=VacancyList, data=vacancy_list_data, config=cls._dacite_config)

        return vacancy_list