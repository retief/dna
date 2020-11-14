from django.db import models

# Create your models here.
class SearchResult(models.Model):
    user_id = models.CharField(max_length=40)
    query = models.CharField(max_length=100)
    protein = models.CharField(max_length=10, blank=True)
    location = models.IntegerField(null=True)
    feature_location = models.CharField(max_length=50, blank=True)
    protein_id = models.CharField(max_length=50, blank=True)
