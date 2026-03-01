from rest_framework.routers import DefaultRouter
from .views import WeeklyPriorityViewSet

router = DefaultRouter()
router.register(r"weekly-priorities", WeeklyPriorityViewSet, basename="weeklypriority")

urlpatterns = router.urls