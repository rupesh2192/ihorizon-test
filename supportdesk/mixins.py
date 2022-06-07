from django.contrib.auth.mixins import AccessMixin


class RoleRequiredMixin(AccessMixin):
    """Verify that the current user has required user type."""
    user_type = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.user_type and not request.user.user_type == self.user_type:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
