from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorPermisssion(BasePermission):
    """
        С этим разрешением:
        - анонимы могут читать
        - пользователи создавать
        - авторы редактировать и удалять
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or request.user and obj.author
            and request.user.is_authenticated
            and request.user == obj.author
        )


class AdminPermission(BasePermission):
    """
        С этим разрешением:
        - анонимы могут читать
        - админы создавать, редактировать и удалять
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class ModeratorPermission(BasePermission):
    """
        С этим разрешением:
        - анонимы могут читать
        - модераторы создавать, редактировать и удалять
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_moderator
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_moderator
        )
