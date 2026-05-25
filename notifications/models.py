from django.db import models
from django.conf import settings

class Notification(models.Model):

    VERB_CHOICES = [
         # Ideas
        ('idea_created',    'Created an idea'),
        ('idea_updated',    'Updated an idea'),
        ('idea_deleted',    'Deleted an idea'),
        ('idea_converted',  'Converted idea to project'),

        # Projects
        ('project_created',   'Created a project'),
        ('project_updated',   'Updated a project'),
        ('project_deleted',   'Deleted a project'),
        ('project_completed', 'Completed a project'),

        # Assignments
        ('assignment_created',   'Created an assignment'),
        ('assignment_completed', 'Completed an assignment'),
        ('assignment_deleted',   'Deleted an assignment'),

        # Skills
        ('skill_created',   'Added a skill'),
        ('skill_practiced', 'Practiced a skill'),
        ('skill_deleted',   'Deleted a skill'),
        ('skill_upgraded',  'Upgraded skill level'),

        # Planning
        ('plan_created', 'Created weekly plan'),
        ('plan_deleted', 'Deleted weekly plan'),
        ('item_done',    'Completed a priority item'),

        # Streak milestones — fired from update_streak()
        ('streak_milestone', 'Hit a streak milestone'),
    ]


    TARGET_TYPE_CHOICES = [
        ('idea',            'Idea'),
        ('project',         'Project'),
        ('assignment',      'Assignment'),
        ('skill',           'Skill'),
        ('weekly_priority', 'Weekly Priority'),
        ('priority_item',   'Priority Item'),
        ('streak',          'Streak'),   # milestone notifications have no DB object
    ]

    #Core fields

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name ='notifications',
    
    )

    verb = models.CharField(
        max_length =50,
        choices =VERB_CHOICES,
    )


    title = models.CharField(max_length = 200)

    body = models.TextField(blank=True, default='')

    is_read = models.BooleanField(default=False)

    #Target -what object this notification is about

    target_type =models.CharField(
        max_length = 20,
        choices =TARGET_TYPE_CHOICES,
        blank =True,
        default = '',

    )

    target_id =models.PositiveIntegerField(
        null =True,
        blank = True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    #Meta

    class Meta:
        ordering =['-created_at']

        indexes = [
            models.Index(fields=['recipient', 'is_read']),

            models.Index(fields=['recipient', 'created_at']),

            models.Index(fields=["recipient", "is_read", "created_at"]),

            models.Index(fields=['verb']),
        ]

    def __str__(self):
        return f"[{self.verb}] - {self.recipient.email} | {self.title}"
    
    #Helper method

    @classmethod
    def create_for_user(cls, user,verb,title,body='', target_type='', target_id=None):
        """
        Clean factory method- signals call this instead of notifications directly.
        One place to add future logic

        Usage in signals:
        Notification.create_for_user(
        user='instace.owner',
        verb='idea_converted',
        title=f"Idea converted to project",
        body=f"'{instace.title}' is now '{project.name}'",
        target_type='project',
        target_id=project.id,
        )
        """
        return cls.objects.create(
            recipient=user,
            verb=verb,
            title=title,
            body=body,
            target_type=target_type,
            target_id=target_id,

        )

