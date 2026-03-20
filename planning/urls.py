from rest_framework.routers import DefaultRouter
from .views import WeeklyPriorityViewSet, WeeklySummaryView, DailyFocusView
from django.urls import path
router = DefaultRouter()
router.register(r"weekly-priorities", WeeklyPriorityViewSet, basename="weeklypriority")

urlpatterns = router.urls + [
    path("planning/weekly-summary/", WeeklySummaryView.as_view(), name="weekly-summary"),
     path("planning/daily-focus/", DailyFocusView.as_view(), name="daily-focus"),
]