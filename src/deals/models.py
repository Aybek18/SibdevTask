from django.db import models

from customers.models import Customer
from gems.models import Gem


class Deal(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="customer_deals"
    )
    item = models.ForeignKey(Gem, on_delete=models.PROTECT, related_name="items")
    total = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    date = models.DateTimeField()
