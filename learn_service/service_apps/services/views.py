from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Subscription, Client
from .serializers import SubscriptionSerializer
from django.db.models import Prefetch

# Create your views here.


class SubscriptionReadOnlyViewSet(ReadOnlyModelViewSet):
    #queryset = Subscription.objects.all().select_related('').only()
    queryset = Subscription.objects.all().select_related('service', 'plan').prefetch_related(
        Prefetch('client',
                 queryset=Client.objects.all().select_related('user').only('company_name', 'user__email')
                 ),
    )
    serializer_class = SubscriptionSerializer
