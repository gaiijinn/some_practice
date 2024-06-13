from django.core.validators import MaxValueValidator
from django.conf import settings
from django.core.cache import cache
from django.db import models

from ..clients.models import Client

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=64)
    full_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.full_price}'


class Plan(models.Model):
    PLAN_TYPE = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount'),
    )

    plan = models.CharField(choices=PLAN_TYPE, max_length=16)
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

    def __str__(self):
        return f'{self.plan} - {self.discount_percent}'


class Subscription(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.PROTECT, related_name='subscription')
    service = models.ForeignKey(to=Service, on_delete=models.PROTECT, related_name='subscription')
    plan = models.ForeignKey(to=Plan, on_delete=models.PROTECT, related_name='subscription')
    price = models.PositiveIntegerField(default=0, blank=True)
    comment = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f'{self.client.company_name} - {self.service.name}'

    def delete(self, using=None, keep_parents=False):
        cache.delete(settings.PRICE_CACHE_NAME)
        super().delete(using=None, keep_parents=False)
