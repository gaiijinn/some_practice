from celery import shared_task


@shared_task()
def math_final_price(subscription_id):
    from .models import Subscription

    subs = Subscription.objects.get(id=subscription_id)
    final_price = (subs.service.full_price -
                   (subs.service.full_price * subs.plan.discount_percent / 100))

    subs.price = final_price
    subs.save()
