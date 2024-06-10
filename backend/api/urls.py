from django.urls import path
from . import views

urlpatterns = [
    path("", views.DatasetListView.as_view(), name="dataset-list"),
    path('<int:pk>/', views.DatasetDetailsView.as_view(), name='dataset-details'),
    path("delete/<int:pk>/", views.DatasetDelete.as_view(), name="dataset-delete"),
]