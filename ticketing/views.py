from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ticketing.models import Topic
from ticketing.permissions import IsIdentified
from ticketing.serializers import TopicSerializer


class TopicListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated, IsIdentified]

    def get_queryset(self):
        return Topic.objects.filter((Q(creator=self.request.user) | Q(supporters__in=[self.request.user])) & Q(
            is_active=True)).distinct().order_by('-id')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)