from django.core.cache import cache
from .models import Permission, Role, UserRole


def get_user_permissions(user):
    if not user.is_authenticated:
        return set()

    cache_key = f'user_permissions_{user.pk}'
    permissions = cache.get(cache_key)

    if permissions is None:
        permissions = set()

        user_roles = Role.objects.filter(user_roles__user=user)
        for role in user_roles:
            for perm in role.permissions.all():
                permissions.add(perm.code)

        cache.set(cache_key, permissions, timeout=3600)

    return permissions


def get_user_roles(user):
    if not user.is_authenticated:
        return Role.objects.none()

    return Role.objects.filter(user_roles__user=user)


def has_permission(user, *codes, require_all=False):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if user.role == 'admin':
        return True

    user_permissions = get_user_permissions(user)

    if require_all:
        return all(code in user_permissions for code in codes)
    return any(code in user_permissions for code in codes)


def invalidate_user_cache(user_id):
    cache_key = f'user_permissions_{user_id}'
    cache.delete(cache_key)


def create_role_with_permissions(name, permission_codes):
    role, created = Role.objects.get_or_create(name=name)
    if created or not role.permissions.exists():
        perms = Permission.objects.filter(code__in=permission_codes)
        role.permissions.set(perms)
    return role


def assign_role_to_user(user, role_name):
    role, _ = Role.objects.get_or_create(name=role_name)
    UserRole.objects.get_or_create(user=user, role=role)
    invalidate_user_cache(user.pk)


def remove_role_from_user(user, role_name):
    role = Role.objects.filter(name=role_name).first()
    if role:
        UserRole.objects.filter(user=user, role=role).delete()
        invalidate_user_cache(user.pk)