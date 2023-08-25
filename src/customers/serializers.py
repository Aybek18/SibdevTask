from rest_framework import serializers

from customers.models import Customer


class CustomerListSerializer(serializers.ModelSerializer):
    spent_money = serializers.IntegerField()
    gems = serializers.ListField()

    class Meta:
        model = Customer
        fields = ("id", "username", "spent_money", "gems")
