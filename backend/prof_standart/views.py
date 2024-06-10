from django.shortcuts import render
from collections import defaultdict
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework import generics
from api.serializers import DatasetSerializer
from rest_framework.permissions import IsAuthenticated

from prof_standart.client import ProfStandartRequestError
from prof_standart.config import PROF_STANDART_CODE_PATH_PARAM, \
    PROF_STANDART_NAME_QUERY_PARAM, \
    PROF_STANDART_NOT_FOUND_ERROR, \
    PROF_STANDART_REQUEST_ERROR
from prof_standart.models import ProfessionalStandart, JobTitle
from prof_standart.serializers import prof_standart_list_to_dict, prof_standart_to_dict
from prof_standart.service import ProfStandartService
from backend.utls import get_page, get_page_size, get_str_path_param, get_str_query_param


class DatasetCreateView(generics.CreateAPIView):
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    _prof_standart_service: ProfStandartService = ProfStandartService()

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            dataset = serializer.save(author=self.request.user)
            prof_standart = request.data['profStandart']
            find_by_code = request.data['findByCode']
            try:
                if (find_by_code == True):
                    prof_standart: ProfessionalStandart = self._prof_standart_service.find_prof_standart_by_code(prof_standart, dataset)
                    result = prof_standart_list_to_dict([prof_standart])
                else:
                    prof_standart_list: [ProfessionalStandart] = self._prof_standart_service.find_prof_standart_by_name(prof_standart, dataset)
                    result = prof_standart_list_to_dict(prof_standart_list)
                result['dataset_id'] = dataset.id
            except ProfStandartRequestError:
                return JsonResponse(data=PROF_STANDART_REQUEST_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except ProfessionalStandart.DoesNotExist:
                return JsonResponse(data=PROF_STANDART_NOT_FOUND_ERROR, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse(result, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
