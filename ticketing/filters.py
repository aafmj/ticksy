from django_filters import rest_framework as filters
from ticketing.models import Ticket


class TicketFilter(filters.FilterSet):

    class Meta:
        model = Ticket
        fields = ['status']
