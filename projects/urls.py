from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, AssignmentViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"assignments", AssignmentViewSet, basename="assignment")
urlpatterns = router.urls