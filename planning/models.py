# planning/models.py

from django.db import models
from core.models import OwnedModel


class WeeklyPriority(OwnedModel):
    week_start = models.DateField()
    top_three_text = models.TextField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Weekly Priority"
        verbose_name_plural = "Weekly Priorities"
        ordering = ["-week_start"]
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["week_start"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "week_start"],
                name="unique_week_per_user"
            )
        ]

    def __str__(self):
        return f"{self.owner.email} - {self.week_start}"