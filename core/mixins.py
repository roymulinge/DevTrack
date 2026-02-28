class OwnerQuerySetMixin:
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)