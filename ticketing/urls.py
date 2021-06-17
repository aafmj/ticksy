from django.urls import path

from ticketing.views import TopicListCreateAPIView

urlpatterns = [
    path('topics/', TopicListCreateAPIView.as_view(), name='topic-list-create'),
]
