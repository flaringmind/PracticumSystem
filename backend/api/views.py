from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from .models import Dataset
from rest_framework import generics
from .serializers import UserSerializer, DatasetSerializer, dataset_to_dict
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class DatasetListView(generics.ListAPIView):
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Dataset.objects.filter(author=user)


class DatasetDelete(generics.DestroyAPIView):
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Dataset.objects.filter(author=user)


class DatasetDetailsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        dataset_id = self.kwargs.get('pk')
        dataset: Dataset = Dataset.objects.get(id=dataset_id)
        cluster_list_response_dict: dict = dataset_to_dict(dataset)
        return JsonResponse(data=cluster_list_response_dict, status=status.HTTP_200_OK)