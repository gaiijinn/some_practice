from django.db import models
from ..clients.models import Client
from django.core.validators import MaxValueValidator

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

    def __str__(self):
        return f'{self.client.name} - {self.service.name}'
