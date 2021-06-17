from django.urls import path

from ticketing.views import TopicListCreateAPIView, EmailListAPIView

urlpatterns = [
    path('topics/', TopicListCreateAPIView.as_view(), name='topic-list-create'),
    path('email/', EmailListAPIView.as_view(), name='email-list'),
]
