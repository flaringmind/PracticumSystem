import math
from typing import Optional

from labor_market.client import HhRuApiClient
from labor_market.dto import VacancyFull, VacancyItem, VacancyList
from labor_market.models import KeySkill, Vacancy, Cluster
from api.models import Dataset
from labor_market.process import ProcessData


class HhRuService:
    _hh_ru_api_client: HhRuApiClient = HhRuApiClient()
    _process_data: ProcessData = ProcessData()
    _page_size: int = 50


    @classmethod
    def _get_and_save_vacancy_from_client(cls, code: int, dataset_obj) -> Optional[KeySkill]:
        try:
            vacancy_full: VacancyFull = cls._hh_ru_api_client.get_vacancy_by_id(vacancy_id=code)
        except VacancyFull.WasNotFound:
            return None

        vacancy_obj: Vacancy = Vacancy(
            code=vacancy_full.id,
            name=vacancy_full.name,
            description=vacancy_full.description,
            dataset=dataset_obj
        )
        vacancy_obj.save()

        key_skills: [KeySkill] = []
        for ks in vacancy_full.key_skills:
            key_skill: KeySkill = KeySkill(name=ks.name, vacancy=vacancy_obj)
            key_skill.save()
            key_skills.append(key_skill)

        return key_skills

    @classmethod
    def _get_and_save_processed_data(cls, codes: [int], dataset_obj) -> [KeySkill]:
        key_skills_list = []
        for code in codes:
            key_skills: [KeySkill] = cls._get_and_save_vacancy_from_client(code, dataset_obj)
            if key_skills:
                [key_skills_list.append(ks.name.lower()) for ks in key_skills]
        print(key_skills_list)
        matrix = cls._process_data.get_tfidf(key_skills_list)
        clusters = cls._process_data.dbscan(matrix)
        processed_data = cls._process_data.get_formatted_data(key_skills_list, clusters)
        print(processed_data)
        for pd in processed_data.values():
            cluster: Cluster = Cluster(cluster_data=pd, dataset=dataset_obj)
            cluster.save()
        return key_skills_list

    @classmethod
    def _find_vacancy_list_from_client(cls, key_words: str, page: int, page_size: int) -> VacancyList:
        vacancy_item_list: VacancyList = cls._hh_ru_api_client.find_vacancies(
            key_words=key_words,
            page=page,
            page_size=page_size
        )
        return vacancy_item_list

    @classmethod
    def get_vacancy(cls, code: int) -> Vacancy:
        vacancy_list: [Vacancy] = cls._get_and_save_processed_data([code])

        if not vacancy_list:
            raise Vacancy.DoesNotExist

        return vacancy_list[0]

    @classmethod
    def find_vacancies(cls, key_words: str, dataset, page: int, page_size: int) -> [KeySkill]:
        pages: int = math.ceil(page_size / cls._page_size)

        all_vacancy_item_list: [VacancyItem] = []
        for p in range(pages):
            vacancy_item_list: VacancyList = cls._find_vacancy_list_from_client(key_words, page + p, cls._page_size)
            all_vacancy_item_list.extend(vacancy_item_list.items)

        codes: [int] = [vi.id for vi in all_vacancy_item_list]
        key_skills_list: [KeySkill] = cls._get_and_save_processed_data(codes, dataset)

        return key_skills_list

    @classmethod
    def find_all_vacancies(cls, key_words: str,  dataset) -> [KeySkill]:
        page: int = 1
        vacancy_item_list: VacancyList = cls._find_vacancy_list_from_client(key_words, page, cls._page_size)
        all_vacancy_item_list: [VacancyItem] = vacancy_item_list.items

        while vacancy_item_list.page < vacancy_item_list.pages:
            page += 1
            vacancy_item_list: VacancyList = cls._find_vacancy_list_from_client(key_words, page, cls._page_size)
            all_vacancy_item_list.extend(vacancy_item_list.items)

        codes: [int] = [vi.id for vi in all_vacancy_item_list]
        key_skills_list: [KeySkill] = cls._get_and_save_processed_data(codes, dataset)

        return key_skills_list
