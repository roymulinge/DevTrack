from django.db import models
from core.models import OwnedModel


class Skill(OwnedModel):
    DEPTH_CHOICES = [
        ('beginner',     'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced',     'Advanced'),
        ('expert',       'Expert'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    depth_level = models.CharField(
        max_length=20,
        choices=DEPTH_CHOICES,
        default='beginner'
    )
    last_practiced = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ['created_at']
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["last_practiced"]),
        ]
    def __str__(self):
        return self.name