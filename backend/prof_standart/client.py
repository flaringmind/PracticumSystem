import time
import humps
import xmltodict

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from prof_standart.config import DaciteConfig, WebDriverConfig
from prof_standart.dto import ProfStandart
from prof_standart.utils import FileReadError, FileUtil


class ProfStandartRequestError(Exception):
    def __init__(self, code: int = None, message: str = None) -> None:
        super().__init__(self, f'profstandart.rosmintrud.ru request error, code: {code}, message: {message}')


class ProfStandartClient:
    _file_util: FileUtil = FileUtil()
    _webdriver_config: WebDriverConfig = WebDriverConfig()
    _dacite_config: DaciteConfig = DaciteConfig()

    _base_url: str = 'profstandart.rosmintrud.ru'
    _prof_standart_registry: str = 'obshchiy-informatsionnyy-blok/natsionalnyy-reestr-' \
                                   'professionalnykh-standartov/reestr-professionalnykh-standartov'
    _prof_standart_url: str = f'https://{_base_url}/{_prof_standart_registry}/'

    _loading_delay: float = 1
    _downloading_delay: float = 1
    _button_value_property: str = 'value'
    _show_button_class: str = 'ps-hide-show'
    _show_button_value: str = 'Развернуть'
    _filter_button_class: str = 'set_filter'
    _download_button_name: str = 'save'
    _download_button_value: str = 'Скачать в XML'

    _code_input_name: str = 'KPF'
    _name_input_name: str = 'NAME'

    @classmethod
    def _download_prof_standart(cls, search_request: str, input_name: str) -> str:
        download_dir: str = cls._file_util.get_download_dir_name(search_request)
        webdriver: WebDriver = cls._webdriver_config.chrome(download_dir)
        webdriver.implicitly_wait(cls._loading_delay)

        try:
            webdriver.get(cls._prof_standart_url)
            show_button = webdriver.find_element(By.CLASS_NAME, cls._show_button_class)

            if show_button.text == cls._show_button_value:
                show_button.click()

            prof_standart_input = webdriver.find_element(By.NAME, input_name)
            prof_standart_input.send_keys(search_request)

            filter_buttons = webdriver.find_element(By.NAME, cls._filter_button_class)
            filter_buttons.click()

            download_buttons = webdriver.find_elements(By.NAME, cls._download_button_name)
            for download_button in download_buttons:
                value = download_button.get_property(cls._button_value_property)
                if value == cls._download_button_value:
                    download_button.click()
                    break

            time.sleep(cls._downloading_delay)
        except TimeoutException:
            raise ProfStandartRequestError(1, f'search request: {search_request}, input name: {input_name}')

        webdriver.quit()

        try:
            return cls._file_util.read_recent_and_remove(download_dir)
        except FileReadError:
            return ''

    @classmethod
    def _get_prof_standarts_from_file(cls, prof_standart_xml: str) -> [dict]:
        prof_standart_data: dict = xmltodict.parse(prof_standart_xml)
        prof_standart_list = prof_standart_data['XMLCardInfo']['ProfessionalStandarts']['ProfessionalStandart']
        prof_standart_list = humps.decamelize(prof_standart_list)
        if isinstance(prof_standart_list, list):
            return prof_standart_list
        else:
            return [prof_standart_list]


    @classmethod
    def find_prof_standart_by_code(cls, code: str) -> ProfStandart:
        prof_standart_xml: str = cls._download_prof_standart(code, cls._code_input_name)

        if not prof_standart_xml:
            raise ProfStandart.WasNotFound(1, f'code: {code}')

        return cls._get_prof_standarts_from_file(prof_standart_xml)[0]

    @classmethod
    def find_prof_standarts_by_name(cls, name: str) -> [ProfStandart]:
        prof_standart_xml: str = cls._download_prof_standart(name, cls._name_input_name)

        if not prof_standart_xml:
            return []

        return cls._get_prof_standarts_from_file(prof_standart_xml)
