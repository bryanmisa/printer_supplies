from django.contrib import messages
from django.shortcuts import redirect


class RoleRequiredMixin:
    allowed_roles = []
    permission_required = None
    redirect_url = 'dashboard'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_superuser or request.user.role == 'admin':
            return super().dispatch(request, *args, **kwargs)

        if request.user.role in self.allowed_roles:
            if self.permission_required:
                if hasattr(request.user, 'has_permission'):
                    if request.user.has_permission(self.permission_required):
                        return super().dispatch(request, *args, **kwargs)
                    else:
                        messages.error(request, 'You do not have permission to access this page.')
                        return redirect(self.redirect_url)
            else:
                return super().dispatch(request, *args, **kwargs)

        messages.error(request, 'You do not have permission to access this page.')
        return redirect(self.redirect_url)