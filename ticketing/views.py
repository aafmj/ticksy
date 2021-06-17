from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ticketing.filters import TicketFilter
from ticketing.models import Topic, Ticket, Message
from ticketing.permissions import IsIdentified, IsTopicOwner, IsTicketOwnerOrAdmin
from ticketing.serializers import TopicSerializer, TicketSerializer, MessageSerializer
from users.models import User, IDENTIFIED
from users.serializers import UserSerializer


class TopicListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, IsIdentified]

    def get_queryset(self):
        return Topic.objects.filter((Q(creator=self.request.user) | Q(supporters__in=[self.request.user])) & Q(
            is_active=True)).distinct().order_by('-id')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class EmailListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsIdentified]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email']

    def get_queryset(self):
        return User.objects.filter(Q(identity__status=IDENTIFIED) & (
                Q(identity__expire_time__isnull=True) |
                Q(identity__expire_time__gt=timezone.now()))).order_by('email')


class TopicRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, IsIdentified, IsTopicOwner]
    http_method_names = ['get', 'patch', 'delete']

    def get_object(self):
        obj = get_object_or_404(Topic, slug=self.kwargs.get('slug'), is_active=True)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminTicketListAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsIdentified]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['id', 'title']
    filterset_class = TicketFilter

    def get_queryset(self):
        return Ticket.objects.filter(Q(topic__slug=self.kwargs.get('slug')) & (
                Q(topic__creator=self.request.user) | Q(topic__supporters__in=[self.request.user])))


class TicketListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['id', 'title']
    filterset_class = TicketFilter

    def get_queryset(self):
        return Ticket.objects.filter(creator=self.request.user)


class TicketRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsTicketOwnerOrAdmin]
    http_method_names = ['patch', 'get']
    queryset = Ticket.objects.all()
    lookup_field = 'id'


class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsTicketOwnerOrAdmin]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return Message.objects.filter(Q(ticket=self.kwargs.get('id'))).order_by('date')
