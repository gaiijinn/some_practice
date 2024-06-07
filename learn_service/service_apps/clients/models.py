from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.PROTECT)
    company_name = models.CharField(max_length=128)
    company_address = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.company_name}'
