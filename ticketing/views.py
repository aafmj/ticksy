from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from ticketing.models import Topic
from ticketing.permissions import IsIdentified
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