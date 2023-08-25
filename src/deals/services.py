import copy

from django.core.cache import cache
from django.db import transaction
from rest_framework.exceptions import ValidationError

from customers.models import Customer
from deals.models import Deal
from gems.models import Gem


class DealService:
    @classmethod
    def save_data(cls, csv_data) -> None:
        content = csv_data.split("\n")
        columns = content[0].strip().split(",")
        received_columns = copy.deepcopy(columns)

        cls.validate_columns(received_columns=received_columns)

        data_to_save = cls.data_to_save(content=content, columns=columns)

        with transaction.atomic():
            Deal.objects.bulk_create(data_to_save)
            cache.delete("cached_customers")

    @classmethod
    def data_to_save(cls, content: list, columns: list) -> list:
        raw_deals = []

        for line in content[1:]:
            values = line.split(",")
            if len(values) != len(columns):
                continue
            ordered_line = dict(zip(columns, values))

            customer, _ = Customer.objects.get_or_create(
                username=ordered_line["customer"]
            )

            item, _ = Gem.objects.get_or_create(name=ordered_line["item"])
            deal = Deal(
                customer=customer,
                item=item,
                total=ordered_line["total"],
                quantity=ordered_line["quantity"],
                date=ordered_line["date"],
            )

            raw_deals.append(deal)
        return raw_deals

    @classmethod
    def validate_columns(cls, received_columns: list) -> None:
        """Сравнение правильности полей"""

        # TODO :
        #  Возможно если в будущем добавиться другие поля для модели Deal этот list comprehension будет показывать
        #  лишние поля, тогда надо будет отрефакторить код, либо статично надо перечислить поля. Пока оставил так ;)

        expected_columns = [
            field.name for field in Deal._meta.get_fields() if field.name != "id"
        ]

        # Для сравнения columns сортируем список по алфавиту
        received_columns.sort()
        expected_columns.sort()

        if received_columns != expected_columns:
            raise ValidationError(
                {
                    "message": "Недопустимые имена столбцов в файле CSV.",
                    "errors": f"Ожидаемые поля {expected_columns} а получены {received_columns}",
                }
            )
