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
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from notifications.models import Notification

@extend_schema_view(
    list=extend_schema(
        summary="List skills",
        description="Retrieve a list of all skills belonging to the authenticated user. Can be filtered by category or searched by name.",
        parameters=[
            OpenApiParameter(
                name="category",
                description="Filter skills by category",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="search",
                description="Search skills by name",
                required=False,
                type=str,
            ),
        ],
    ),
    create=extend_schema(
        summary="Create a skill",
        description="Create a new skill to track. The authenticated user will be set as the owner.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a skill",
        description="Retrieve details of a specific skill by its ID.",
    ),
    update=extend_schema(
        summary="Update a skill",
        description="Update all fields of an existing skill.",
    ),
    partial_update=extend_schema(
        summary="Partially update a skill",
        description="Update specific fields of an existing skill.",
    ),
    destroy=extend_schema(
        summary="Delete a skill",
        description="Delete a skill permanently.",
    ),
)
class SkillViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category"]
    search_fields = ["name"]
    ordering_fields = ["created_at"]
    
    def perform_create(self, serializer):
        skill = serializer.save(owner=self.request.user)

        Notification.create_for_user(
            user=self.request.user,
            verb="skill_created",
            title="Skill added",
            body=f"'{skill.name}' was added to your skills.",
            target_type="skill",
            target_id=skill.id,
        )


    def perform_destroy(self, instance):
        name = instance.name
        skill_id = instance.id

        instance.delete()

        Notification.create_for_user(
            user=self.request.user,
            verb="skill_deleted",
            title="Skill deleted",
            body=f"'{name}' was deleted.",
            target_type="skill",
            target_id=skill_id,
        )

    @extend_schema(
        summary="Get stale skills",
        description="Retrieve the 10 most stale skills that haven't been practiced in 90+ days or have never been practiced.",
    )
    @action(detail=False, methods=["get"])
    def stale(self, request):
        threshold = timezone.now().date() - timedelta(days=90)

        stale_skills = (self.get_queryset().filter(
            models.Q(last_practiced__lt=threshold) |
            models.Q(last_practiced__isnull=True)
        )
         .order_by("last_practiced")[:10]
    )

        serializer = self.get_serializer(stale_skills, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Mark skill as practiced",
        description="One-click action to mark a skill as practiced today. Updates the last_practiced timestamp to the current date.",
    )
    @action(detail=True, methods=["post"])
    def practice(self, request, pk=None):
        """One click — marks skill as practiced today"""
        skill = self.get_object()
        skill.last_practiced = timezone.now().date()
        skill.save()

        Notification.create_for_user(
            user=request.user,
            verb="skill_practiced",
            title="Skill practiced",
            body=f"You practiced '{skill.name}' today.",
            target_type="skill",
            target_id=skill.id,
        )
        serializer = self.get_serializer(skill)
        return Response(serializer.data)