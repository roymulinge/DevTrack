from django.db import models
from core.models import OwnedModel


class Idea(OwnedModel):
    title = models.CharField(max_length=200, default="Untitled Idea")
    problem_statement = models.TextField()
    target_user = models.CharField(max_length=200)
    revenue_model = models.CharField(max_length=200)
    complexity_score = models.PositiveSmallIntegerField()

    status = models.CharField(
        max_length=30,
        default="draft"
    )

    related_project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ideas"
    )

    related_skills = models.ManyToManyField(
        "skills.Skill",
        blank=True,
        related_name="ideas"
    )
    class Meta:
        verbose_name = "Idea"
        verbose_name_plural = "Ideas"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["complexity_score"]),
        ]

    def __str__(self):
        return self.problem_statement[:50]