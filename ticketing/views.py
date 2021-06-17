from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ticketing.models import Topic
from ticketing.permissions import IsIdentified, IsTopicOwner
from ticketing.serializers import TopicSerializer
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