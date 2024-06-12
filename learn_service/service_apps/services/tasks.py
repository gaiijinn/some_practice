from celery import shared_task
from django.db.models import F
from celery_singleton import Singleton
import time


@shared_task(base=Singleton)  # Для того чтобы не запускать одну таску много раз с такими же аргументами
def math_final_price(subscription_id):
    from .models import Subscription
    time.sleep(5)
    subs = Subscription.objects.filter(id=subscription_id).annotate(
        annotated_price=(F('service__full_price') -
                         F('service__full_price') * F('plan__discount_percent') / 100.00)).first()

    subs.price = subs.annotated_price
    subs.save()
