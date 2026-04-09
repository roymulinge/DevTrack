# core/dashboard.py
from django.utils import timezone          # ← correct Django timezone
from datetime import timedelta             # ← standard library timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from planning.models import WeeklyPriority
from projects.models import Project, Assignment
from skills.models import Skill
from ideas.models import Idea

# Import brief serializers for lightweight dashboard responses
from projects.serializer import (
    AssignmentBriefSerializer,   # id, title, status, deadline
    SkillBriefSerializer,        # id, name, category, depth_level
    ProjectBriefSerializer,      # id, name, status, priority
)
from planning.serializer import WeeklyPrioritySerializer


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]  # ← blocks unauthenticated requests

    def get(self, request):
        user = request.user                              # who is logged in
        now  = timezone.now()                            # current datetime (timezone-aware)
        today = now.date()                               # just the date part
        seven_days_ago = today - timedelta(days=7)       # 7 days back from today
        week_start = today - timedelta(days=today.weekday())  # Monday of current week

        # ── Overdue assignments ──────────────────────────
        # select_related fetches project and skill in same DB query (no N+1)
        overdue = Assignment.objects.filter(
            owner=user,
            deadline__lt=now,                            # deadline is in the past
            status__in=['not_started', 'in_progress']   # not yet done
        ).select_related('project', 'related_skill')[:5]

        # ── Stale skills ─────────────────────────────────
        stale_skills = Skill.objects.filter(
            owner=user,
            last_practiced__lt=seven_days_ago            # not practiced in 7 days
        )[:5]

        # ── Active projects ───────────────────────────────
        # prefetch_related fetches assignments and skills in separate queries
        # but avoids N+1 — better than select_related for ManyToMany
        active_projects = Project.objects.filter(
            owner=user,
            status='active'
        ).prefetch_related('assignments', 'skills')[:5]

        # ── This week's WeeklyPriority ────────────────────
        weekly = WeeklyPriority.objects.filter(
            owner=user,
            week_start=week_start
        ).prefetch_related('items').first()              # .first() returns None if not found

        # ── Focus score — the intelligence layer ─────────
        focus = self._compute_focus(overdue, stale_skills)

        return Response({
            "counts": {
                # Simple counts for dashboard summary cards
                "projects":    Project.objects.filter(owner=user).count(),
                "skills":      Skill.objects.filter(owner=user).count(),
                "assignments": Assignment.objects.filter(owner=user).count(),
                "ideas":       Idea.objects.filter(owner=user).count(),
            },
            "overdue_assignments": AssignmentBriefSerializer(overdue, many=True).data,
            "stale_skills":        SkillBriefSerializer(stale_skills, many=True).data,
            "active_projects":     ProjectBriefSerializer(active_projects, many=True).data,
            "this_week": WeeklyPrioritySerializer(weekly).data if weekly else None,
            "focus": focus,
        })

    def _compute_focus(self, overdue, stale_skills):
        """
        Intelligence layer — returns the single most important action.

        Priority rules:
        1. CRITICAL — overdue assignment whose skill is also stale
        2. HIGH     — any overdue assignment
        3. MEDIUM   — any stale skill
        4. CLEAR    — nothing urgent, suggest planning
        """
        # Build a set of stale skill IDs for O(1) lookup
        # Using a set means checking membership is instant regardless of size
        stale_skill_ids = {s.id for s in stale_skills}

        # Rule 1 — worst case: overdue work AND skill out of practice
        for assignment in overdue:
            if assignment.related_skill_id in stale_skill_ids:
                return {
                    "level":   "critical",
                    "message": (
                        f"'{assignment.title}' is overdue and its skill "
                        f"'{assignment.related_skill.name}' hasn't been "
                        f"practiced in 7+ days. Address this first."
                    ),
                    "type": "assignment",
                    "id":   assignment.id,
                }

        # Rule 2 — overdue work exists
        if overdue:
            first = overdue[0]
            return {
                "level":   "high",
                "message": f"'{first.title}' is overdue. Focus on this next.",
                "type":    "assignment",
                "id":      first.id,
            }

        # Rule 3 — skill going stale
        if stale_skills:
            skill = stale_skills[0]
            return {
                "level":   "medium",
                "message": f"'{skill.name}' hasn't been practiced in 7+ days.",
                "type":    "skill",
                "id":      skill.id,
            }

        # Rule 4 — all clear
        return {
            "level":   "clear",
            "message": "You're on track. Plan your week if you haven't already.",
            "type":    "planning",
            "id":      None,
        }