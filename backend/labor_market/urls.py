from django.urls import path
from . import views

urlpatterns = [
    path("", views.VacancyListAPIView.as_view(), name="vacancies"),
]