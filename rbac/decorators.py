from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def require_permission(*codes, require_all=False, login_url=None, next_param='next'):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                login_url = login_url or '/login/'
                return redirect(f'{login_url}?{next_param}={request.path}')

            if hasattr(request.user, 'has_permission'):
                if request.user.has_permission(*codes, require_all=require_all):
                    return view_func(request, *args, **kwargs)

            if request.user.role == 'admin' or request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard')
        return wrapper
    return decorator


def require_role(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/login/')

            if request.user.is_superuser or request.user.role == 'admin':
                return view_func(request, *args, **kwargs)

            if request.user.role in roles:
                return view_func(request, *args, **kwargs)

            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard')
        return wrapper
    return decorator


def admin_required(view_func):
    return require_role('admin')(view_func)


def manager_required(view_func):
    return require_role('admin', 'manager')(view_func)


def staff_required(view_func):
    return require_role('admin', 'manager', 'staff')(view_func)