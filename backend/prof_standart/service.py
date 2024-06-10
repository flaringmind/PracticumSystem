from typing import Optional
from prof_standart.client import ProfStandartClient
from prof_standart.dto import ProfStandart
from prof_standart.models import JobTitle, ProfessionalStandart


class ProfStandartService:
    _prof_standart_client: ProfStandartClient = ProfStandartClient()

    @classmethod
    def _get_job_title(cls, job_titles, pjt, ps_obj):
        if pjt not in [jt.name for jt in job_titles]:
            job_title: JobTitle = JobTitle(name=pjt, profstandart=ps_obj)
            job_title.save()
            job_titles.append(job_title)

    @classmethod
    def _get_and_save_professional_standart(cls, prof_standart: ProfStandart, found_by: str, dataset_obj) -> str:
        professional_standart: ProfessionalStandart = ProfessionalStandart(
            code=prof_standart['first_section']['code_kind_professional_activity'],
            name=prof_standart['name_professional_standart'],
            found_by=found_by,
            dataset=dataset_obj
        )
        professional_standart.save()
        job_titles: [str] = []
        pjts: [str] = []
        for gwf in prof_standart['third_section']['work_functions']['generalized_work_functions']['generalized_work_function']:
            if isinstance(gwf, dict) and gwf['possible_job_titles']:
                if isinstance(gwf['possible_job_titles']['possible_job_title'], list):
                    for pjt in gwf['possible_job_titles']['possible_job_title']:
                        cls._get_job_title(job_titles, pjt, professional_standart)
                        pjts.append(pjt)
                else:
                    pjt: str = gwf['possible_job_titles']['possible_job_title']
                    cls._get_job_title(job_titles, pjt, professional_standart)
                    pjts.append(pjt)
        return professional_standart

    @classmethod
    def _get_and_save_prof_standart_by_code_from_client(cls, code: str, dataset) -> Optional[ProfessionalStandart]:
        try:
            prof_standart: dict = cls._prof_standart_client.find_prof_standart_by_code(code)
        except ProfStandart.WasNotFound:
            return None
        professional_standart = cls._get_and_save_professional_standart(prof_standart, code, dataset)

        return professional_standart

    @classmethod
    def _get_and_save_prof_standarts_by_name_from_client(cls, name: str, dataset) -> [ProfessionalStandart]:
        try:
            prof_standart_list: [dict] = cls._prof_standart_client.find_prof_standarts_by_name(name)
        except ProfStandart.WasNotFound:
            return []
        professional_standart_list: [dict] = []
        for prof_standart in prof_standart_list:
            professional_standart = cls._get_and_save_professional_standart(prof_standart, name, dataset)
            professional_standart_list.append(professional_standart)

        return professional_standart_list

    @classmethod
    def find_prof_standart_by_code(cls, code: str, dataset) -> ProfessionalStandart:
        professional_standart: ProfessionalStandart = cls._get_and_save_prof_standart_by_code_from_client(code, dataset)

        if not professional_standart:
            raise ProfessionalStandart.DoesNotExist

        return professional_standart

    @classmethod
    def find_prof_standart_by_name(cls, name: str, dataset):
        prof_standart_list: [ProfessionalStandart] = cls._get_and_save_prof_standarts_by_name_from_client(name, dataset)
        return prof_standart_list

