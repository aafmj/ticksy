import datetime

from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404

from ticketing.models import Ticket
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


class IsTicketOwnerOrAdmin(permissions.BasePermission):
    message = 'شما سازنده یا ادمین این تیکت نیستید.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        user = request.user
        ticket = get_object_or_404(Ticket, id=view.kwargs.get('id'))
        return (user == ticket.topic.creator) or (user in ticket.topic.supporters) or (user == ticket.creator)


class IsTicketCreator(permissions.BasePermission):
    message = 'فقط سازنده های تیکت ها میتوانند به پیام ادمین ها رتبه دهند.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_object_permission(self, request, view, obj):
        return request.user == obj.ticket.creator
