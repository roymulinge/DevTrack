from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid
from notifications.models import Notification
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Email verification
    email_verified          = models.BooleanField(default=False)
    verification_token      = models.UUIDField(default=uuid.uuid4, editable=False)
    verification_token_created = models.DateTimeField(auto_now_add=True)
    
    # Streak Tracking 
    current_streak = models.PositiveIntegerField(default=0) #how many consecutive days the user has been active RIGHT NOW
    longest_streak = models.PositiveIntegerField(default=0) # the personal best - never decreses, motivational record
    last_active_date = models.DateField(null=True, blank=True) # the date of the last completion action - used to calculate if streak continues
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email  

    def update_streak(self):
        """
        Call this whenever the user completes any action.
        Handles three cases: first ever action, continuing streak and broken streak
        """  
        from django.utils import timezone
        today = timezone.now.date()

        if self.last_active_date is None:
            # Case 1 user has never completed anything

            self.current_streak = 1

        elif self.last_active_date == today:
            #Case 2 user already did something today
            # don't double-count stay as it is 
            return
        
        elif (today - self.last_active_date).days == 1:
            #Case 3 last action was Yesterday - streak continues

            self.current_streak +=1

        else:
            #Case 4 gap of 2+ days - streak is broken
            
            self.current_streak = 1
        
        #Update longest_streak if current just beat the record
    
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
       
        #save the three fields 

        self.save(update_fields= [
            'current_streak',
            'longest_streak',
            'last_active_date'
        ])

        Notification.create_for_user(
            user=User,
            verb="streak_milestone",
            title="Streak milestone reached",
            body=f"You hit a {self.current_streak}-day streak!",
            target_type="streak",
            target_id=None,
        )
