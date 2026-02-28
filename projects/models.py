from django.db import models
from core.models import OwnedModel
from django.db.models import Q
# Create your models here.
class Project(OwnedModel):
    name = models.CharField(max_length=200)
    vision = models.TextField()
    priority = models.IntegerField()
    status = models.CharField(
        max_length=30,
        choices=[
            ('active', 'Active'),
            ('paused', 'Paused'),
            ('completed', 'Completed'),
        ],
        default='active'
    )

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.name

class Assignment(OwnedModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="assignments"
    )
    subject = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    effort_estimate = models.IntegerField()
    completed = models.BooleanField(default=False)

    related_skill = models.ForeignKey(
        "skills.Skill",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assignments"
    )

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
        ordering = ["deadline"]
        constraints = [
            models.CheckConstraint(
                condition= Q(effort_estimate__gte=0),
                name="positive_effort_estimate"
            )
        ]
        indexes = [
            models.Index(fields=["deadline"]),
            models.Index(fields=["completed"]),
        ]
    def __str__(self):
        return self.title