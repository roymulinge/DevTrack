from django.db import models
from core.models import OwnedModel

# Create your models here.
class Project(OwnedModel):
    name = models.CharField(max_length=200)
    vision = models.TextField()
    priority = models.IntegerField()
    status = models.CharField(max_length=50)

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
        blank=True
    )

    def __str__(self):
        return self.title