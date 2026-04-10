from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeeklyPriorityViewSet, PriorityItemViewSet, WeeklySummaryView, DailyFocusView, NextActionView

router = DefaultRouter()
router.register(r"weekly-priorities",  WeeklyPriorityViewSet,  basename="weekly-priorities")
router.register(r"priority-items",     PriorityItemViewSet,    basename="priority-items")

urlpatterns = [
    path("", include(router.urls)),
    path("planning/weekly-summary/", WeeklySummaryView.as_view(), name="weekly-summary"),
    path("planning/daily-focus/",    DailyFocusView.as_view(),    name="daily-focus"),
    path("planning/next-action/",    NextActionView.as_view(),    name="next-action"),
    path("planning/priority-items/", include(router.urls)),
]