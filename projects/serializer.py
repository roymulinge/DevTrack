from rest_framework import serializers
from .models import Project, Assignment
from skills.models import Skill


class SkillBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Skill
        fields = ["id", "name", "category", "depth_level"]


class AssignmentBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Assignment
        fields = ["id", "title", "status", "deadline"]


class ProjectSerializer(serializers.ModelSerializer):
    skills_detail = SkillBriefSerializer(source="skills", many=True, read_only=True)
    skills        = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all(), required=False)
    assignments   = AssignmentBriefSerializer(many=True, read_only=True)
    progress      = serializers.SerializerMethodField()

    def get_progress(self, obj):
        total     = obj.assignments.count()
        completed = obj.assignments.filter(status="completed").count()
        if total == 0:
            return {"total": 0, "completed": 0, "percent": 0}
        return {
            "total":     total,
            "completed": completed,
            "percent":   round((completed / total) * 100),
        }

    class Meta:
        model  = Project
        fields = [
            "id", "name", "vision", "priority", "status",
            "skills", "skills_detail",
            "assignments", "progress",       # ✅ added
            "created_at", "updated_at",
        ]
        read_only_fields = ["owner", "created_at", "updated_at"]


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Assignment
        fields = [
            "id", "project", "subject", "title", "deadline",
            "status",        # ✅ replaces completed
            "related_skill", "owner", "created_at", "updated_at"
        ]
        read_only_fields = ["owner", "created_at", "updated_at"]