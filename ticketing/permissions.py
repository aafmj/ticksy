import datetime

from rest_framework import permissions, status

from users.models import IDENTIFIED


class IsIdentified(permissions.BasePermission):
    message = 'هویت شما هنوز توسط ادمین تایید نشده است.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        user = request.user
        if not hasattr(user, 'identity'):
            return False
        return (user.identity.status == IDENTIFIED and (
            user.identity.expire_time > datetime.datetime.now() if user.identity.expire_time else True)) or user.is_superuser
        # return request.user.is_identified()


class IsTopicOwner(permissions.BasePermission):
    message = 'شما سازنده این تاپیک نیستید.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
