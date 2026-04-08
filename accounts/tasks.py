from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from psycopg import logger


@shared_task
def send_overdue_reminders():
    from .models import User
    from .emails import send_overdue_reminder
    from projects.models import Assignment

    now = timezone.now()
    users = User.objects.filter(is_active=True, email_verified=True)

    for user in users:
        overdue = Assignment.objects.filter(
            owner=user,
            deadline__lt=now,
            completed=False,
        )
        if overdue.exists():
            try:
                send_overdue_reminder(user, list(overdue))
            except Exception as e:
                logger.error(f"Overdue reminder error for {user.email}: {e}")


@shared_task
def send_stale_skill_reminders():
    from .models import User
    from .emails import send_stale_skills_reminder
    from skills.models import Skill

    cutoff = timezone.now().date() - timedelta(days=7)
    users  = User.objects.filter(is_active=True, email_verified=True)

    for user in users:
        stale = Skill.objects.filter(
            owner=user,
            last_practiced__lt=cutoff,
        )
        if stale.exists():
            try:
                send_stale_skills_reminder(user, list(stale))
            except Exception as e:
                print(f"Stale skills error for {user.email}: {e}")


@shared_task
def send_weekly_reminders():
    from .models import User
    from .emails import send_weekly_reminder
    from planning.models import WeeklyPriority

    users = User.objects.filter(is_active=True, email_verified=True)

    for user in users:
        # Get this week's priorities
        today      = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())

        latest = WeeklyPriority.objects.filter(
            owner=user,
            week_start=week_start,
        ).first()

        priorities = []
        if latest and latest.top_three_text:
            priorities = [
                line.strip()
                for line in latest.top_three_text.split("\n")
                if line.strip()
            ]

        try:
            send_weekly_reminder(user, priorities)
        except Exception as e:
            print(f"Weekly reminder error for {user.email}: {e}")