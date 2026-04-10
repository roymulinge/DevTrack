from django.db import models
from django.utils import timezone
from core.models import OwnedModel


class Project(OwnedModel):
    name     = models.CharField(max_length=200)
    vision   = models.TextField(blank=True, default="")
    priority = models.CharField(
        max_length=20,
        choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')],
        default='medium'
    )
    status = models.CharField(
        max_length=30,
        choices=[('active', 'Active'), ('paused', 'Paused'), ('completed', 'Completed')],
        default='active'
    )
    skills = models.ManyToManyField("skills.Skill", blank=True, related_name="projects")

    class Meta:
        verbose_name        = "Project"
        verbose_name_plural = "Projects"
        ordering            = ["-created_at"]
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.name


class Assignment(OwnedModel):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed',   'Completed'),
    ]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,
        related_name="assignments", null=True, blank=True,
    )
    subject       = models.CharField(max_length=200, blank=True, default="")
    title         = models.CharField(max_length=200)
    deadline      = models.DateTimeField(null=True, blank=True)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    related_skill = models.ForeignKey(
        "skills.Skill", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="assignments"
    )

    def save(self, *args, **kwargs):
        if self.project:
            self.owner = self.project.owner
        if self.deadline and timezone.is_naive(self.deadline):
            self.deadline = timezone.make_aware(self.deadline)
        super().save(*args, **kwargs)

    @property
    def completed(self):
        return self.status == 'completed'

    class Meta:
        verbose_name        = "Assignment"
        verbose_name_plural = "Assignments"
        ordering            = ["deadline"]
        indexes = [
            models.Index(fields=["deadline"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.title