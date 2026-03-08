from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.mixins import OwnerQuerySetMixin
from core.permissions import IsOwner
from .models import WeeklyPriority
from .serializer import WeeklyPrioritySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class WeeklyPriorityViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset = WeeklyPriority.objects.all()
    serializer_class = WeeklyPrioritySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
   
    search_fields = ["notes", "top_three_text", "week_start"]
    ordering_fields = ["priority", "created_at"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)