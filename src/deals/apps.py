from django.apps import AppConfig


class DealsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "deals"

    def ready(self) -> None:
        import deals.signals  # Noqa
