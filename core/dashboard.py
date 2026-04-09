from django.utils import timezone


from rest_framework.views import APIView
from rest_framework.response import Response
from planning.models import WeeklyPriority
from projects.models import Project, Assignment
from skills.models import Skill
from ideas.models import Idea
from rest_framework.permissions import IsAuthenticated
from projects.serializer import AssignmentSerializer
from skills.serializer import SkillSerializer  
from projects.serializer import ProjectSerializer
from planning.serializer import WeeklyPrioritySerializer


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        
        user = request.user
        now = timezone.now()
        today = now.date()
        seven_days = today - timedelta(days=7)
        week_start = today - timedelta(days=today.weekday())


        # ── Overdue assignments ──────────────────────────────
        overdue = Assignment.objects.filter(
            owner=user,
            deadline__lt=now,
            status__in=['not_started', 'in_progress']
        ).select_related('project', 'related_skill')[:5]

        # ── Stale skills ─────────────────────────────────────
        stale_skills = Skill.objects.filter(
            owner=user,
            last_practiced__lt=seven_days
        )[:5]

        # ── Active projects with progress ────────────────────
        active_projects = Project.objects.filter(
            owner=user,
            status='active'
        ).prefetch_related('assignments', 'skills')[:5]

        # ── This week's priorities ───────────────────────────
        weekly = WeeklyPriority.objects.filter(
            owner=user,
            week_start=week_start
        ).prefetch_related('items').first()

        # ── FOCUS SCORE — the intelligence ───────────────────
        # What should you work on RIGHT NOW?
        focus = self._compute_focus(user, overdue, stale_skills)
        return Response({
            "counts": {
                "projects":   Project.objects.filter(owner=user).count(),
                "skills":     Skill.objects.filter(owner=user).count(),
                "assignments": Assignment.objects.filter(owner=user).count(),
                "ideas":      Idea.objects.filter(owner=user).count(),
            },
            "overdue_assignments": AssignmentBriefSerializer(overdue, many=True).data,
            "stale_skills": SkillBriefSerializer(stale_skills, many=True).data,
            "active_projects": ProjectBriefSerializer(active_projects, many=True).data,
            "this_week": WeeklyPrioritySerializer(weekly).data if weekly else None,
            "focus": focus,
        })

    def _compute_focus(self, user, overdue, stale_skills):
        """
        Simple intelligence — surfaces the single most important thing.
        Rules (in priority order):
        1. Overdue assignment + its skill is stale = CRITICAL
        2. Overdue assignment = HIGH
        3. Stale skill linked to active project = MEDIUM  
        4. Nothing urgent = suggest weekly planning
        """
        stale_skill_ids = {s.id for s in stale_skills}

        for assignment in overdue:
            if assignment.related_skill_id in stale_skill_ids:
                return {
                    "level": "critical",
                    "message": f"'{assignment.title}' is overdue and its skill "
                               f"'{assignment.related_skill.name}' hasn't been "
                               f"practiced in 7+ days. Address this first.",
                    "type": "assignment",
                    "id": assignment.id
                }

        if overdue:
            first = overdue[0]
            return {
                "level": "high",
                "message": f"'{first.title}' is overdue. Focus on this next.",
                "type": "assignment",
                "id": first.id
            }

        if stale_skills:
            skill = stale_skills[0]
            return {
                "level": "medium",
                "message": f"'{skill.name}' hasn't been practiced in 7+ days.",
                "type": "skill",
                "id": skill.id
            }

        return {
            "level": "clear",
            "message": "You're on track. Plan your week if you haven't already.",
            "type": "planning",
            "id": None
        }