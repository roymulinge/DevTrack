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

class ProjectViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "priority"]
    search_fields = ["name", "vision"]
    ordering_fields = ["priority", "created_at"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AssignmentViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"])
    def overdue(self, request):

        overdue_assignments = (self.get_queryset().filter(
            deadline__lt=timezone.now(),
            completed=False
        )
         .order_by("deadline")[:10]
    )

        serializer = self.get_serializer(overdue_assignments, many=True)
        return Response(serializer.data)