from rest_framework import serializers
from .models import WeeklyPriority


class WeeklyPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyPriority
        fields = "__all__"
        read_only_fields = ["owner"]