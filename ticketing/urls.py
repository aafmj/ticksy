from django.urls import path

from ticketing.views import TopicListCreateAPIView, EmailListAPIView, TopicRetrieveUpdateDestroyAPIView, \
    AdminTicketListAPIView, TicketListCreateAPIView, TicketRetrieveUpdateAPIView

urlpatterns = [
    path('topics/', TopicListCreateAPIView.as_view(), name='topic-list-create'),
    path('email/', EmailListAPIView.as_view(), name='email-list'),
    path('topics/<slug:slug>/', TopicRetrieveUpdateDestroyAPIView.as_view(), name='topic-retrieve-update-destroy'),
    path('topics/<slug:slug>/tickets/', AdminTicketListAPIView.as_view(), name='admin-ticket-list'),

    path('tickets/', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('tickets/<int:id>/', TicketRetrieveUpdateAPIView.as_view(), name='ticket-detail'),
]
