from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Plan, Service
from .tasks import math_final_price


def price_updater(instance: object):
    for subs in instance.subscription.all():
        math_final_price.delay(subs.id)


@receiver(post_save, sender=Plan)
def update_price_plan_subs(sender, instance, created, **kwargs):
    if not created:
        price_updater(instance)


@receiver(post_save, sender=Service)
def update_price_plan_subs(sender, instance, created, **kwargs):
    if not created:
        price_updater(instance)
