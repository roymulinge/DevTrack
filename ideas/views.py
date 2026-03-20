from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.mixins import OwnerQuerySetMixin
from core.permissions import IsOwner
from .models import Idea
from .serializer import IdeaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from projects.models import Project


class IdeaViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["problem_statement", "target_user", "revenue_model"]
    ordering_fields = ["created_at"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def convert(self, request, pk=None):
        """Convert an idea into a project"""
        idea = self.get_object()

        # Don't convert if already linked to a project
        if idea.related_project:
            return Response(
                {"error": "This idea is already linked to a project."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create project from idea
        project = Project.objects.create(
            owner=request.user,
            name=idea.problem_statement[:200],  # use problem as project name
            vision=f"Originally from idea: {idea.problem_statement}",
            priority="medium",
            status="active",
        )

        # Link idea to project and mark as in progress
        idea.related_project = project
        idea.status          = "in_progress"
        idea.save()

        return Response({
            "message":    "Idea converted to project successfully!",
            "project_id": project.id,
            "project":    project.name,
        }, status=status.HTTP_201_CREATED)