from django.urls import path
from . import views

urlpatterns = [
    path("", views.DatasetCreateView.as_view(), name="dataset-create"),
]