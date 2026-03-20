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
class WeeklyPriorityViewSet(OwnerQuerySetMixin, ModelViewSet):
    queryset = WeeklyPriority.objects.all()
    serializer_class = WeeklyPrioritySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
   
    search_fields = ["notes", "top_three_text", "week_start"]
    ordering_fields = ["priority", "created_at"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class WeeklySummaryView(APIView):

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