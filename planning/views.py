from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.mixins import OwnerQuerySetMixin
from core.permissions import IsOwner
from .models import WeeklyPriority
from .serializer import WeeklyPrioritySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from projects.models import Assignment, Project
from skills.models import Skill
from django.db import models
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        summary="List weekly priorities",
        description="Retrieve a list of weekly priority entries for the authenticated user.",
    ),
    create=extend_schema(
        summary="Create weekly priority entry",
        description="Create a new weekly priority entry. The authenticated user will be set as the owner.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a weekly priority entry",
        description="Retrieve details of a specific weekly priority entry by its ID.",
    ),
    update=extend_schema(
        summary="Update a weekly priority entry",
        description="Update all fields of an existing weekly priority entry.",
    ),
    partial_update=extend_schema(
        summary="Partially update a weekly priority entry",
        description="Update specific fields of an existing weekly priority entry.",
    ),
    destroy=extend_schema(
        summary="Delete a weekly priority entry",
        description="Delete a weekly priority entry permanently.",
    ),
)
class WeeklyPriorityViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset = WeeklyPriority.objects.all()
    serializer_class = WeeklyPrioritySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
   
    search_fields = ["notes", "top_three_text", "week_start"]
    ordering_fields = ["priority", "created_at"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@extend_schema(
    summary="Get weekly summary",
    description="Retrieve a summary of the current week's productivity including completed assignments, overdue assignments, active projects, and skills practiced."
)
class WeeklySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        today = timezone.now().date()
        week_start = today - timedelta(days=7)

        completed = Assignment.objects.filter(
            owner=request.user,
            status='completed',
            deadline__gte=week_start
        ).count()

        overdue = Assignment.objects.filter(
            owner=request.user,
            status__in=['not_started', 'in_progress'],
            deadline__lt=today
        ).count()

        active_projects = Project.objects.filter(
            owner=request.user,
            status="active"
        ).count()

        practiced_skills = Skill.objects.filter(
            owner=request.user,
            last_practiced__gte=week_start
        ).count()

        return Response({
            "completed_assignments": completed,
            "overdue_assignments": overdue,
            "active_projects": active_projects,
            "skills_practiced_this_week": practiced_skills
        })

@extend_schema(
    summary="Get daily focus dashboard",
    description="Retrieve a daily dashboard showing urgent assignments due soon, stale skills needing practice, and projects with overdue work."
)
class DailyFocusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today     = timezone.now()
        soon      = today + timedelta(days=3)
        stale_threshold = today.date() - timedelta(days=7)

        # Assignments due soon or overdue and not completed
        urgent_assignments = Assignment.objects.filter(
            owner=request.user,
            deadline__lte=soon,
            status__in=["not_started", "in_progress"]
        ).order_by("deadline")[:5]

        # Stale skills
        stale_skills = Skill.objects.filter(
            owner=request.user,
        ).filter(
            models.Q(last_practiced__lt=stale_threshold) |
            models.Q(last_practiced__isnull=True)
        ).order_by("last_practiced")[:3]

        # Projects with overdue assignments
        overdue_projects = Project.objects.filter(
            owner=request.user,
            status="active",
            assignments__deadline__lt=today,
            assignments__status__in=["not_started", "in_progress"]
        ).distinct()[:3]

        return Response({
            "urgent_assignments": [
                {
                    "id":       a.id,
                    "title":    a.title,
                    "deadline": a.deadline,
                    "status":   a.status,
                    "days":     (a.deadline.date() - today.date()).days if a.deadline else None,
                }
                for a in urgent_assignments
            ],
            "stale_skills": [
                {
                    "id":             s.id,
                    "name":           s.name,
                    "last_practiced": s.last_practiced,
                    "days_ago":       (today.date() - s.last_practiced).days if s.last_practiced else None,
                }
                for s in stale_skills
            ],
            "overdue_projects": [
                {
                    "id":   p.id,
                    "name": p.name,
                }
                for p in overdue_projects
            ],
            "total_urgent": urgent_assignments.count() + stale_skills.count(),
        })

class NextActionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        # 1. Priority: any active project that has an assignment due soon (next 3 days)
        soon = today + timedelta(days=3)
        urgent_assignment = Assignment.objects.filter(
            owner=user,
            deadline__date__lte=soon,
            deadline__date__gte=today,
            status__in=['not_started', 'in_progress']
        ).select_related('project').order_by('deadline').first()

        if urgent_assignment and urgent_assignment.project:
            return Response({
                'type': 'assignment',
                'id': urgent_assignment.id,
                'name': urgent_assignment.title,
                'project_id': urgent_assignment.project.id,
                'project_name': urgent_assignment.project.name,
            })

        # 2. Next: any active project that has been updated recently (last 7 days)
        recent_project = Project.objects.filter(
            owner=user,
            status='active'
        ).order_by('-updated_at').first()

        if recent_project:
            return Response({
                'type': 'project',
                'id': recent_project.id,
                'name': recent_project.name,
            })

        # 3. Fallback: any assignment that is overdue
        overdue_assign = Assignment.objects.filter(
            owner=user,
            deadline__lt=today,
            status__in=['not_started', 'in_progress']
        ).order_by('deadline').first()

        if overdue_assign:
            return Response({
                'type': 'assignment',
                'id': overdue_assign.id,
                'name': overdue_assign.title,
            })

        # 4. No action found
        return Response({'type': None})