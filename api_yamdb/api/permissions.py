from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Доступ к чтению разрешён всем, а изменение — только администраторам.
    """

    def has_permission(self, request, view):
        # Разрешаем доступ всем только для методов "чтения"
        # таких как (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Проверяем, что пользователь авторизован
        if request.user.is_authenticated:
            # Для остальных методов (POST, PUT, DELETE) разрешаем админам
            return request.user.is_admin
        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_superuser


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
            or obj.author == request.user
        )
