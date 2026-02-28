from django.db import models
from core.models import OwnedModel


class Skill(OwnedModel):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    depth_level = models.PositiveSmallIntegerField()
    last_practiced = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["last_practiced"]),
        ]
    def __str__(self):
        return self.name