from labor_market.models import Vacancy
from backend.serializer import get_list_response_dict


def vacancy_to_dict(vacancy: Vacancy) -> dict:
    return {
        'code': vacancy.code,
        'name': vacancy.name,
        'keyskills': [ks.name for ks in vacancy.keyskills.all()]
    }


def vacancy_list_to_dict(page: int, page_size: int, vacancy_list: [Vacancy]) -> dict:
    return get_list_response_dict(page, page_size, [vacancy_to_dict(v) for v in vacancy_list])
