# planning/models.py

from django.db import models
from core.models import OwnedModel


class WeeklyPriority(OwnedModel):
    week_start = models.DateField()
    
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
    

class PriorityItem(OwnedModel):
    # Each item IS a real thing in the system
    weekly_priority = models.ForeignKey(
        WeeklyPriority,
        on_delete=models.CASCADE,
        related_name="items"
    )
    order = models.PositiveSmallIntegerField()  # 1, 2, 3
    text = models.CharField(max_length=300)     # fallback plain text

    # Link to real objects — all optional
    linked_project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    linked_assignment = models.ForeignKey(
        "projects.Assignment",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    linked_skill = models.ForeignKey(
        "skills.Skill",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]