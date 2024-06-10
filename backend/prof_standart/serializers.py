from prof_standart.models import ProfessionalStandart
from backend.serializer import get_list_response_dict


def prof_standart_to_dict(prof_standart: ProfessionalStandart) -> dict:
    return {
        'code': prof_standart.code,
        'name': prof_standart.name,
        'job_titles': [jt.name for jt in prof_standart.job_titles.all().order_by('name')]
    }


def prof_standart_list_to_dict(prof_standart_list: [ProfessionalStandart]) -> dict:
    return {'pslist': [prof_standart_to_dict(v) for v in prof_standart_list]}


