from django.db import models
from api.models import Dataset


class Vacancy(models.Model):
    code = models.CharField(max_length=255)
    created = models.DateField(auto_now=True)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=50000, null=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="vacancies")
    
    class Meta:
        db_table = 'vacancy'


class KeySkill(models.Model):
    name = models.CharField(max_length=255)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="keyskills")

    class Meta:
        db_table = 'keyskill'


class Cluster(models.Model):
    cluster_data = models.CharField(max_length=10000)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="clusters")

    class Meta:
        db_table = 'cluster'
