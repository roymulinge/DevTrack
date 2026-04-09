from rest_framework import serializers
from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Idea
        # Explicit fields — never use __all__ in production
        # __all__ exposes new fields automatically when you add them
        # which can leak data you didn't intend to expose
        fields = [
            "id", "title", "problem_statement", "target_user",
            "revenue_model", "complexity_score", "status",
            "related_project", "related_skills",
            "owner", "created_at", "updated_at"
        ]
        read_only_fields = ["owner", "created_at", "updated_at"]