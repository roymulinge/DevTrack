from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.mixins import OwnerQuerySetMixin
from core.permissions import IsOwner
from .models import Idea
from .serializer import IdeaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class IdeaViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)