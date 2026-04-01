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
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample

@extend_schema_view(
    list=extend_schema(
        summary="List ideas",
        description="Retrieve a list of all ideas belonging to the authenticated user. Can be filtered by status and searched by problem statement, target user, or revenue model.",
        parameters=[
            OpenApiParameter(
                name="status",
                description="Filter ideas by status (e.g., backlog, in_progress, completed)",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="search",
                description="Search ideas by problem statement, target user, or revenue model",
                required=False,
                type=str,
            ),
        ],
    ),
    create=extend_schema(
        summary="Create an idea",
        description="Create a new idea. The authenticated user will be set as the owner.",
    ),
    retrieve=extend_schema(
        summary="Retrieve an idea",
        description="Retrieve details of a specific idea by its ID.",
    ),
    update=extend_schema(
        summary="Update an idea",
        description="Update all fields of an existing idea.",
    ),
    partial_update=extend_schema(
        summary="Partially update an idea",
        description="Update specific fields of an existing idea.",
    ),
    destroy=extend_schema(
        summary="Delete an idea",
        description="Delete an idea permanently.",
    ),
)
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

    @extend_schema(
        summary="Convert idea to project",
        description="Convert an idea into a new project. The idea will be linked to the project and its status will be updated to 'in_progress'. An idea can only be converted if it's not already linked to a project.",
        responses={
            201: OpenApiExample(
                "Success Response",
                value={
                    "message": "Idea converted to project successfully!",
                    "project_id": 1,
                    "project": "Project Name"
                }
            ),
            400: OpenApiExample(
                "Error Response",
                value={"error": "This idea is already linked to a project."}
            ),
        }
    )
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