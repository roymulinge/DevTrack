from django.db import models
from core.models import OwnedModel
from django.db.models import Q

class Project(OwnedModel):
    name     = models.CharField(max_length=200)
    vision   = models.TextField(blank=True, default="")   # ← allow empty
    priority = models.CharField(                          # ← string not int
        max_length=20,
        choices=[
            ('high',   'High'),
            ('medium', 'Medium'),
            ('low',    'Low'),
        ],
        default='medium'
    )
    status = models.CharField(
        max_length=30,
        choices=[
            ('active',    'Active'),
            ('paused',    'Paused'),
            ('completed', 'Completed'),
        ],
        default='active'
    )
    skills = models.ManyToManyField(
        "skills.Skill",
        blank=True,
        related_name="projects"
    )

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
        Project,
        on_delete=models.CASCADE,
        related_name="assignments",
        null=True,              # ← allow no project
        blank=True,
    )
    subject         = models.CharField(max_length=200, blank=True, default="")
    title           = models.CharField(max_length=200)
    deadline        = models.DateTimeField(null=True, blank=True)   # ← optional
       #  Removed effort_estimate
    status       = models.CharField(         # ✅ replaces completed boolean
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started'
    )

    related_skill = models.ForeignKey(
        "skills.Skill",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assignments"
    )

    def save(self, *args, **kwargs):
        if self.project:
            self.owner = self.project.owner
        super().save(*args, **kwargs)

    @property
    def completed(self):
        """Backward compatibility — so existing code doesnt break"""
        return self.status == 'completed'

    class Meta:
        verbose_name        = "Assignment"
        verbose_name_plural = "Assignments"
        ordering            = ["deadline"]
        
        indexes = [
            models.Index(fields=["deadline"]),
            models.Index(fields=["completed"]),
        ]

    def __str__(self):
        return self.title