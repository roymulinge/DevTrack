from rest_framework import serializers
from .models import Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "category", "depth_level", "last_practiced", "notes", "owner", "created_at"]
        read_only_fields = ["owner", "created_at"]