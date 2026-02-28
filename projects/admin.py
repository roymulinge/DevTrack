from django.contrib import admin
from .models import Project, Assignment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "priority", "status", "created_at")
    search_fields = ("name",)
    list_filter = ("status", "priority")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "owner", "deadline", "completed")
    list_filter = ("completed", "deadline")