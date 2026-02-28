from rest_framework.routers import DefaultRouter
from .views import IdeaViewSet

router = DefaultRouter()
router.register(r"ideas", IdeaViewSet)

urlpatterns = router.urls