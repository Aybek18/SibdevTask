from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=40, unique=True)
