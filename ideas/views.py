from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.mixins import OwnerQuerySetMixin
from core.permissions import IsOwner
from .models import Idea
from .serializer import IdeaSerializer


class IdeaViewSet(OwnerQuerySetMixin, ModelViewSet):
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)