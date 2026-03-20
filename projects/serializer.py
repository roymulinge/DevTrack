from rest_framework import serializers
from .models import Project, Assignment
from skills.models import Skill

class SkillBriefSerializer(serializers.ModelSerializer):
    """Lightweight skill info shown inside a project"""
    class Meta:
        model = Skill
        fields = ["id", "name", "category", "depth_level"]

class ProjectSerializer(serializers.ModelSerializer):
     skills_detail = SkillBriefSerializer(source="skills", many=True, read_only=True)

     skills = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Skill.objects.all(),
        required=False
    )
     class Meta:
           model = Project
           fields = ["id", "name", "vision", "priority", "status", "skills", "skills_detail", "created_at", "updated_at", "owner"]
           read_only_fields = ["owner", "created_at", "updated_at"]

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ["id", "project", "subject", "title", "deadline", "completed", "related_skill", "owner", "created_at", "updated_at"]
        read_only_fields = ["owner", "created_at", "updated_at"]