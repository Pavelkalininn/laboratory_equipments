from django.core.exceptions import PermissionDenied


def is_staff_user(function):
    """Возвращает 403 ошибку если у юзера нет прав доступа staff."""

    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return wrapper
