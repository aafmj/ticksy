from django.urls import path

from ticketing.views import TopicListCreateAPIView, EmailListAPIView, TopicRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('topics/', TopicListCreateAPIView.as_view(), name='topic-list-create'),
    path('email/', EmailListAPIView.as_view(), name='email-list'),
    path('topics/<slug:slug>/', TopicRetrieveUpdateDestroyAPIView.as_view(), name='topic-retrieve-update-destroy'),
]
