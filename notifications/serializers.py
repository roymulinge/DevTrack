from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "verb",
            "title",
            "body",
            "is_read",
            "target_type",
            "target_id",
            "created_at",
        ]
        read_only_fields = fields