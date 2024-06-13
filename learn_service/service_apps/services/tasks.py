import datetime
import time
from django.core.cache import cache
from django.conf import settings
from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.db.models import F


#@shared_task(base=Singleton)  # Для того чтобы не запускать одну таску много раз с такими же аргументами, а только первую
@shared_task()
def math_final_price(subscription_id):
    from .models import Subscription

    with transaction.atomic():
        # sleep нужен чтобы воспровести ошибку при который паралельные таски не до конца применяют изменения
        time.sleep(5)

        # получим доступ после заверешния блока транзакции в set_comment
        subs = Subscription.objects.select_for_update().filter(id=subscription_id).annotate(
            annotated_price=(F('service__full_price') -
                             F('service__full_price') * F('plan__discount_percent') / 100.00)).first()
        time.sleep(25)
        subs.price = subs.annotated_price
        subs.save()

    cache.delete(settings.PRICE_CACHE_NAME)


@shared_task()
def set_comment(subscription_id):
    from .models import Subscription

    with transaction.atomic():  # блокируем доступ пока транзакция не закончится
        subs = Subscription.objects.select_for_update().get(id=subscription_id)
        if subs:
            time.sleep(27)
            subs.comment = str(datetime.datetime.now())
            subs.save()

    cache.delete(settings.PRICE_CACHE_NAME)
