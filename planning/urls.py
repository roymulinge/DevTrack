from rest_framework.routers import DefaultRouter
from .views import WeeklyPriorityViewSet, WeeklySummaryView
from django.urls import path
router = DefaultRouter()
router.register(r"weekly-priorities", WeeklyPriorityViewSet, basename="weeklypriority")

urlpatterns = router.urls + [
    path("planning/weekly-summary/", WeeklySummaryView.as_view(), name="weekly-summary"),
]