from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from api.models import Dataset
from rest_framework.permissions import IsAuthenticated

from labor_market.client import HhRuRequestError
from labor_market.config import KEY_WORDS_QUERY_PARAM, VACANCY_CODE_PATH_PARAM, \
    VACANCY_NOT_FOUND_ERROR, \
    VACANCY_REQUEST_ERROR
from labor_market.models import Vacancy
from labor_market.serializers import vacancy_list_to_dict, vacancy_to_dict
from labor_market.service import HhRuService
from backend.utls import get_int_path_param, get_page, get_page_size, get_str_query_param


class VacancyListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    _hh_ru_service: HhRuService = HhRuService()

    def post(self, request: Request, *args, **kwargs):
        page: int = get_page(request)
        page_size: int = get_page_size(request)

        dataset_id = request.data['dataset_id']
        dataset: Dataset = Dataset.objects.get(id=dataset_id)
        key_words = request.data['profession']

        try:
            self._hh_ru_service.find_vacancies(key_words, dataset, page, page_size)
        except HhRuRequestError:
            return JsonResponse(data=VACANCY_REQUEST_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse({}, status=status.HTTP_200_OK)