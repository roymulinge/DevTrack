from rest_framework import serializers
from .models import WeeklyPriority, PriorityItem


class PriorityItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PriorityItem
        fields = [
            "id", "order", "text", "is_done",
            "linked_project", "linked_assignment", "linked_skill"
        ]
        # owner and weekly_priority set automatically — not exposed to frontend


class WeeklyPrioritySerializer(serializers.ModelSerializer):
    # Nested items — when you GET a WeeklyPriority you get all its items
    items = PriorityItemSerializer(many=True, read_only=True)

    class Meta:
        model  = WeeklyPriority
        fields = [
            "id", "week_start", "notes",
              
            "items",           # new structured items
            "owner", "created_at", "updated_at"
        ]
        read_only_fields = ["owner", "created_at", "updated_at"]