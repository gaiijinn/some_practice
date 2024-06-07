from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Subscription
from .serializers import SubscriptionSerializer

# Create your views here.


class SubscriptionReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().select_related('client', 'service').prefetch_related('client__user')
    serializer_class = SubscriptionSerializer
    