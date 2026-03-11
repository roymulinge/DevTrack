from rest_framework.views import APIView
from rest_framework.response import Response
from projects.models import Project, Assignment
from skills.models import Skill
from ideas.models import Idea


class DashboardView(APIView):

    def get(self, request):

        user = request.user

        return Response({
            "projects": Project.objects.filter(owner=user).count(),
            "skills": Skill.objects.filter(owner=user).count(),
            "ideas": Idea.objects.filter(owner=user).count(),
            "assignments_total": Assignment.objects.filter(owner=user).count(),
            "assignments_completed": Assignment.objects.filter(
                owner=user,
                completed=True
            ).count(),
        })