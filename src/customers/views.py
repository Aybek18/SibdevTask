from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from customers.models import Customer
from customers.serializers import CustomerListSerializer
from customers.services import CustomerService


class CustomerListAPIView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer

    def get(self, request, *args, **kwargs):
        cached_data = cache.get("cached_customers")
        if cached_data is not None:
            return Response(cached_data, status=status.HTTP_200_OK)

        customer_list = CustomerService.get_top_5_customers(
            queryset=self.get_queryset()
        )
        serializer = CustomerListSerializer(customer_list, many=True)
        cache.set(
            "cached_customers",
            serializer.data,
            timeout=settings.CACHE_EXPIRATION_SECONDS,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
