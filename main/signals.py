from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save

from . import models


@receiver([pre_delete, pre_save], sender=models.News)
def news_update(sender, instance, **kwargs):
    cache.delete("news")
    cache.delete(f"post_{instance.slug}")


@receiver([pre_delete, pre_save], sender=models.Page)
def page_update(sender, instance, **kwargs):
    cache.delete("menu")
    cache.delete(f"page_{instance.slug}")


@receiver([pre_delete, pre_save], sender=models.Banner)
def banner_update(sender, instance, **kwargs):
    cache.delete("banners")
