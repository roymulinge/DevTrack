from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.mixins import OwnerQuerySetMixin
from core.permissions import IsOwner
from .models import WeeklyPriority
from .serializer import WeeklyPrioritySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class WeeklyPriorityViewSet(OwnerQuerySetMixin, ModelViewSet):
    serializer_class = WeeklyPrioritySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "priority"]
    search_fields = ["name", "description"]
    ordering_fields = ["priority", "created_at"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)