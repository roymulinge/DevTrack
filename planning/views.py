from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.mixins import OwnerQuerySetMixin
from core.permissions import IsOwner
from .models import WeeklyPriority, PriorityItem
from .serializer import WeeklyPrioritySerializer, PriorityItemSerializer
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
from notifications.models import Notification

@extend_schema_view(
    list=extend_schema(summary="List weekly priorities"),
    create=extend_schema(summary="Create weekly priority entry"),
    retrieve=extend_schema(summary="Retrieve a weekly priority entry"),
    update=extend_schema(summary="Update a weekly priority entry"),
    partial_update=extend_schema(summary="Partially update a weekly priority entry"),
    destroy=extend_schema(summary="Delete a weekly priority entry"),
)
class WeeklyPriorityViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset           = WeeklyPriority.objects.all()
    serializer_class   = WeeklyPrioritySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields      = ["notes", "week_start"]
    ordering_fields    = ["week_start", "created_at"]

    def perform_create(self, serializer):
        weekly_priority = serializer.save(owner=self.request.user)

        Notification.create_for_user(
            user=self.request.user,
            verb="plan_created",
            title="Weekly plan created",
            body=f"Weekly plan for {weekly_priority.week_start} was created.",
            target_type="weekly_priority",
            target_id=weekly_priority.id,
        )


    def perform_destroy(self, instance):
        week_start = instance.week_start
        weekly_priority_id = instance.id

        instance.delete()

        Notification.create_for_user(
            user=self.request.user,
            verb="plan_deleted",
            title="Weekly plan deleted",
            body=f"Weekly plan for {week_start} was deleted.",
            target_type="weekly_priority",
            target_id=weekly_priority_id,
        )


@extend_schema_view(
    list=extend_schema(summary="List priority items"),
    create=extend_schema(summary="Create a priority item"),
    retrieve=extend_schema(summary="Retrieve a priority item"),
    update=extend_schema(summary="Update a priority item"),
    partial_update=extend_schema(summary="Partially update a priority item"),
    destroy=extend_schema(summary="Delete a priority item"),
)
class PriorityItemViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset           = PriorityItem.objects.all()
    serializer_class   = PriorityItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends    = [DjangoFilterBackend]
    filterset_fields   = ["weekly_priority"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def perform_update(self, serializer):
        old_done = self.get_object().done
        item = serializer.save()

        if old_done is False and item.done is True:
            Notification.create_for_user(
                user=self.request.user,
                verb="is_done",
                title="Priority item completed",
                body=f"'{item.title}' was completed.",
                target_type="priority_item",
                target_id=item.id,
            )


@extend_schema(summary="Get weekly summary")
class WeeklySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today      = timezone.now().date()
        week_start = today - timedelta(days=7)

        completed = Assignment.objects.filter(
            owner=request.user,
            status='completed',
            deadline__date__gte=week_start
        ).count()

        overdue = Assignment.objects.filter(
            owner=request.user,
            status__in=['not_started', 'in_progress'],
            deadline__date__lt=today
        ).count()

        active_projects = Project.objects.filter(
            owner=request.user, status="active"
        ).count()

        practiced_skills = Skill.objects.filter(
            owner=request.user, last_practiced__gte=week_start
        ).count()

        return Response({
            "completed_assignments":      completed,
            "overdue_assignments":        overdue,
            "active_projects":            active_projects,
            "skills_practiced_this_week": practiced_skills,
        })


@extend_schema(summary="Get daily focus dashboard")
class DailyFocusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today           = timezone.now().date()
        soon            = today + timedelta(days=3)
        stale_threshold = today - timedelta(days=7)

        urgent_assignments = Assignment.objects.filter(
            owner=request.user,
            deadline__date__lte=soon,
            status__in=["not_started", "in_progress"]
        ).order_by("deadline")[:5]

        stale_skills = Skill.objects.filter(
            owner=request.user,
        ).filter(
            models.Q(last_practiced__lt=stale_threshold) |
            models.Q(last_practiced__isnull=True)
        ).order_by("last_practiced")[:3]

        overdue_projects = Project.objects.filter(
            owner=request.user,
            status="active",
            assignments__deadline__date__lt=today,
            assignments__status__in=["not_started", "in_progress"]
        ).distinct()[:3]

        return Response({
            "urgent_assignments": [
                {
                    "id":       a.id,
                    "title":    a.title,
                    "deadline": a.deadline,
                    "status":   a.status,
                    "days":     (a.deadline.date() - today).days if a.deadline else None,
                }
                for a in urgent_assignments
            ],
            "stale_skills": [
                {
                    "id":             s.id,
                    "name":           s.name,
                    "last_practiced": s.last_practiced,
                    "days_ago":       (today - s.last_practiced).days if s.last_practiced else None,
                }
                for s in stale_skills
            ],
            "overdue_projects": [
                {"id": p.id, "name": p.name}
                for p in overdue_projects
            ],
            "total_urgent": urgent_assignments.count() + stale_skills.count(),
        })


class NextActionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user  = request.user
        today = timezone.now().date()
        soon  = today + timedelta(days=3)

        urgent_assignment = Assignment.objects.filter(
            owner=user,
            deadline__date__lte=soon,
            deadline__date__gte=today,
            status__in=['not_started', 'in_progress']
        ).select_related('project').order_by('deadline').first()

        if urgent_assignment and urgent_assignment.project:
            return Response({
                'type':         'assignment',
                'id':           urgent_assignment.id,
                'name':         urgent_assignment.title,
                'project_id':   urgent_assignment.project.id,
                'project_name': urgent_assignment.project.name,
            })

        recent_project = Project.objects.filter(
            owner=user, status='active'
        ).order_by('-updated_at').first()

        if recent_project:
            return Response({'type': 'project', 'id': recent_project.id, 'name': recent_project.name})

        overdue_assign = Assignment.objects.filter(
            owner=user,
            deadline__date__lt=today,
            status__in=['not_started', 'in_progress']
        ).order_by('deadline').first()

        if overdue_assign:
            return Response({'type': 'assignment', 'id': overdue_assign.id, 'name': overdue_assign.title})

        return Response({'type': None})