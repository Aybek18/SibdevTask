from rest_framework import serializers

from deals.models import Deal


class DealCreateSerializer(serializers.Serializer):
    deals = serializers.FileField()

    def validate_deals(self, value):
        """Валидация на тип загружаемого контента"""

        if not value.name.endswith(".csv"):
            raise serializers.ValidationError(
                "Загруженный файл не является CSV файлом."
            )
        return value


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = (
            "user",
            "gem",
            "quantity",
        )
