class OwnerQuerySetMixin:
    """
    Automatically filters queryset to objects owned by request.user.
    Works for list, retrieve, and custom actions.
    """
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self.request, "user") and self.request.user.is_authenticated:
            return qs.filter(owner=self.request.user)
        return qs.none()  # unauthenticated users see nothing