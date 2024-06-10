from django.db import models
from api.models import Dataset

class ProfessionalStandart(models.Model):
    code = models.CharField(max_length=255)
    created = models.DateField(auto_now=True)
    name = models.CharField(max_length=500)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="profstandarts")
    found_by = models.CharField(max_length=500)

    class Meta:
        db_table = 'professionalstandart'

class JobTitle(models.Model):
    name = models.CharField(max_length=500)
    profstandart = models.ForeignKey(ProfessionalStandart, on_delete=models.CASCADE, related_name="job_titles")

    class Meta:
        db_table = 'jobtitle'
