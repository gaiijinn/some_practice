from django.db.models import F, Prefetch, Sum
from django.core.cache import cache
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ReadOnlyModelViewSet


from .models import Client, Subscription
from .serializers import SubscriptionSerializer

# Create your views here.


class SubscriptionReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().select_related('service', 'plan').prefetch_related(
        Prefetch('client',
                 queryset=Client.objects.all().select_related('user').only('company_name', 'user__email')
                 )).order_by('-id')

    serializer_class = SubscriptionSerializer

    #@method_decorator(cache_page(60 * 2))
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_sum = price_cache
        else:
            total_sum = self.get_queryset().aggregate(total=Sum('price'))
            cache.set(settings.PRICE_CACHE_NAME, total_sum, 60)

        # уровень питона
        response_data = {'result': response.data, 'total_sum': total_sum}
        response.data = response_data  # делаем вложеность

        return response
