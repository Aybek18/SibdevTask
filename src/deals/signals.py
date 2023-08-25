from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from deals.models import Deal


@receiver([post_delete, post_save], sender=Deal)
def clear_cache_on_model_modification(sender, instance, **kwargs):
    cache.delete("cached_customers")
