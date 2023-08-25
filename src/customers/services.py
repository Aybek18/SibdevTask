from typing import List

from django.db.models import QuerySet, Sum

from customers.models import Customer
from deals.models import Deal


class CustomerService:
    @classmethod
    def get_top_5_customers(cls, queryset: QuerySet[Customer]) -> List[Customer]:
        top_five_customers = queryset.annotate(
            spent_money=Sum("customer_deals__total")
        ).order_by("-spent_money")[:5]

        unique_bought_gems = cls.get_unique_bought_gems(
            top_five_customers=top_five_customers
        )

        filtered_bought_gems = cls.get_gems_with_two_customers_or_more(
            unique_bought_gems=unique_bought_gems
        )

        return cls.get_customers_with_gems(
            top_five_customers=top_five_customers,
            filtered_bought_gems=filtered_bought_gems,
        )

    @classmethod
    def get_unique_bought_gems(cls, top_five_customers: QuerySet[Customer]) -> dict:
        # Получаем уникальные проданные камни по типу [название камня, клиент]
        gems = (
            Deal.objects.filter(customer__in=top_five_customers)
            .values_list("item__name", "customer_id")
            .distinct()
        )
        # Группируем камни по названию
        similar_gems_dict = {}

        for gem_name, customer_id in gems:
            if gem_name in similar_gems_dict:
                similar_gems_dict[gem_name].append(customer_id)
            else:
                similar_gems_dict[gem_name] = [customer_id]
        return similar_gems_dict

    @classmethod
    def get_gems_with_two_customers_or_more(cls, unique_bought_gems) -> dict:
        # Фильтруем камни, оставляем только те, которые были куплены как минимум двумя покупателями

        return {
            gem_name: count
            for gem_name, count in unique_bought_gems.items()
            if len(count) >= 2
        }

    @classmethod
    def get_customers_with_gems(
        cls, top_five_customers, filtered_bought_gems
    ) -> List[dict]:
        customers = list(top_five_customers.values())
        # Добавляем ключ 'gems' с соответствующим списком из второго словаря
        for user in customers:
            user_id = user["id"]
            user["gems"] = [
                key for key, value in filtered_bought_gems.items() if user_id in value
            ]
        return customers
