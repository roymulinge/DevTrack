from rest_framework import serializers
from .models import Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "category", "depth_level", "last_practiced", "notes", "owner", "created_at"]
        read_only_fields = ["owner", "created_at"]

class SkillBriefSerializer(serializers.ModelSerializer):
    # Lightweight serializer — used in dashboard and project relations
    # Only returns what the dashboard needs, keeps response fast
    class Meta:
        model = Skill
        fields = ["id", "name", "category", "depth_level", "last_practiced"]