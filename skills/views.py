from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db import models
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.mixins import OwnerQuerySetMixin
from core.permissions import IsOwner
from .models import Skill
from .serializer import SkillSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class SkillViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category"]
    search_fields = ["name"]
    ordering_fields = ["created_at"]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"])
    def stale(self, request):
        threshold = timezone.now().date() - timedelta(days=90)

        stale_skills = self.get_queryset().filter(
            models.Q(last_practiced__lt=threshold) |
            models.Q(last_practiced__isnull=True)
        )

        serializer = self.get_serializer(stale_skills, many=True)
        return Response(serializer.data)