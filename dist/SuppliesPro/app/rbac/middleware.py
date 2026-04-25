from django.utils.deprecation import MiddlewareMixin


class RBACMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request.user, 'is_authenticated'):
            return None

        if request.user.is_authenticated:
            from .services import get_user_permissions, get_user_roles

            request.user.rbac_permissions = get_user_permissions(request.user)
            request.user.rbac_roles = list(get_user_roles(request.user).values_list('name', flat=True))

            def has_permission(*codes, require_all=False):
                from .services import has_permission
                return has_permission(request.user, *codes, require_all=require_all)

            def has_role(*roles):
                if not request.user.is_authenticated:
                    return False
                if request.user.is_superuser or request.user.role == 'admin':
                    return True
                return request.user.role in roles

            request.user.has_permission = has_permission
            request.user.has_role = has_role

        return None