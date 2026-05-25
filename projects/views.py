from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.mixins import OwnerQuerySetMixin
from core.permissions import IsOwner
from .models import Project
from .serializer import ProjectSerializer, AssignmentSerializer
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Assignment
from .serializer import AssignmentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from notifications.models import Notification

@extend_schema_view(
    list=extend_schema(
        summary="List projects",
        description="Retrieve a list of all projects belonging to the authenticated user. Can be filtered by status and priority, or searched by name and vision.",
        parameters=[
            OpenApiParameter(
                name="status",
                description="Filter projects by status (e.g., active, completed, on_hold)",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="priority",
                description="Filter projects by priority (e.g., low, medium, high)",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="search",
                description="Search projects by name or vision",
                required=False,
                type=str,
            ),
        ],
    ),
    create=extend_schema(
        summary="Create a project",
        description="Create a new project. The authenticated user will be set as the owner.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a project",
        description="Retrieve details of a specific project by its ID.",
    ),
    update=extend_schema(
        summary="Update a project",
        description="Update all fields of an existing project.",
    ),
    partial_update=extend_schema(
        summary="Partially update a project",
        description="Update specific fields of an existing project.",
    ),
    destroy=extend_schema(
        summary="Delete a project",
        description="Delete a project permanently.",
    ),
)
class ProjectViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "priority"]
    search_fields = ["name", "vision"]
    ordering_fields = ["priority", "created_at"]

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)

        Notification.create_for_user(
            user=self.request.user,
            verb="project_created",
            title="Project created",
            body=f"'{project.name}' was created.",
            target_type="project",
            target_id=project.id,
        )


    def perform_update(self, serializer):
        old_status = self.get_object().status
        project = serializer.save()

        if old_status != "completed" and project.status == "completed":
            verb = "project_completed"
            title = "Project completed"
            body = f"'{project.name}' was marked as completed."
        else:
            verb = "project_updated"
            title = "Project updated"
            body = f"'{project.name}' was updated."

        Notification.create_for_user(
            user=self.request.user,
            verb=verb,
            title=title,
            body=body,
            target_type="project",
            target_id=project.id,
        )


    def perform_destroy(self, instance):
        name = instance.name
        project_id = instance.id

        instance.delete()

        Notification.create_for_user(
            user=self.request.user,
            verb="project_deleted",
            title="Project deleted",
            body=f"'{name}' was deleted.",
            target_type="project",
            target_id=project_id,
        )

@extend_schema_view(
    list=extend_schema(
        summary="List assignments",
        description="Retrieve a list of all assignments belonging to the authenticated user.",
    ),
    create=extend_schema(
        summary="Create an assignment",
        description="Create a new assignment (task). The authenticated user will be set as the owner.",
    ),
    retrieve=extend_schema(
        summary="Retrieve an assignment",
        description="Retrieve details of a specific assignment by its ID.",
    ),
    update=extend_schema(
        summary="Update an assignment",
        description="Update all fields of an existing assignment.",
    ),
    partial_update=extend_schema(
        summary="Partially update an assignment",
        description="Update specific fields of an existing assignment.",
    ),
    destroy=extend_schema(
        summary="Delete an assignment",
        description="Delete an assignment permanently.",
    ),
)
class AssignmentViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        assignment = serializer.save(owner=self.request.user)

        Notification.create_for_user(
            user=self.request.user,
            verb="assignment_created",
            title="Assignment created",
            body=f"'{assignment.title}' was created.",
            target_type="assignment",
            target_id=assignment.id,
        )


    def perform_update(self, serializer):
        old_status = self.get_object().status
        assignment = serializer.save()

        if old_status != "completed" and assignment.status == "completed":
            Notification.create_for_user(
                user=self.request.user,
                verb="assignment_completed",
                title="Assignment completed",
                body=f"'{assignment.title}' was marked as completed.",
                target_type="assignment",
                target_id=assignment.id,
            )


    def perform_destroy(self, instance):
        title = instance.title
        assignment_id = instance.id

        instance.delete()

        Notification.create_for_user(
            user=self.request.user,
            verb="assignment_deleted",
            title="Assignment deleted",
            body=f"'{title}' was deleted.",
            target_type="assignment",
            target_id=assignment_id,
        )

    @extend_schema(
        summary="Get overdue assignments",
        description="Retrieve the 10 most urgent overdue or in-progress assignments with deadlines in the past.",
    )
    @action(detail=False, methods=["get"])
    def overdue(self, request):

        overdue_assignments = (self.get_queryset().filter(
            deadline__lt=timezone.now(),
            status__in=['not_started', 'in_progress']
        )
         .order_by("deadline")[:10]
    )

        serializer = self.get_serializer(overdue_assignments, many=True)
        return Response(serializer.data)