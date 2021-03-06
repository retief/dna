from django.db import models

# Create your models here.
class SearchResult(models.Model):
    """The results of a given search.  If everything is null, the search is in
    progress or failed."""

    user_id = models.CharField(max_length=40)
    query = models.CharField(max_length=100)
    genome = models.CharField(max_length=10, blank=True)
    location = models.IntegerField(null=True)
    feature_location = models.CharField(max_length=50, blank=True)
    protein_id = models.CharField(max_length=50, blank=True)

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "query": self.query,
            "genome": self.genome,
            "location": self.location,
            "feature_location": self.feature_location,
            "protein_id": self.protein_id,
        }
