from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="datasets")

    class Meta:
        db_table = 'dataset'

    def __str__(self):
        return self.title

