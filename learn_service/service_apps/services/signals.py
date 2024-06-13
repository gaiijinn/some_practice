from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Plan, Service, Subscription
from .tasks import math_final_price, set_comment


def price_updater(instance: object):
    for subs in instance.subscription.all():
        math_final_price.delay(subs.id)
        set_comment.delay(subs.id)


@receiver(post_save, sender=Plan)
def update_price_plan_subs(sender, instance, created, **kwargs):
    if not created:
        price_updater(instance)


@receiver(post_save, sender=Service)
def update_price_plan_subs(sender, instance, created, **kwargs):
    if not created:
        price_updater(instance)


@receiver(post_save, sender=Subscription)
def set_price_comment(sender, instance, created, **kwargs):
    if created:
        math_final_price.delay(instance.id)
        set_comment.delay(instance.id)
