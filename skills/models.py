from django.db import models
from core.models import OwnedModel


class Skill(OwnedModel):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    depth_level = models.IntegerField()
    last_practiced = models.DateField()

    def __str__(self):
        return self.name