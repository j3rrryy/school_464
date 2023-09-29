from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.core.cache import cache

from .models import *


@receiver([pre_delete, pre_save], sender=News)
def news_update(sender, instance, **kwargs):
    cache.delete('news')
    cache.delete(f'post_{instance.slug}')

@receiver([pre_delete, pre_save], sender=Page)
def page_update(sender, instance, **kwargs):
    cache.delete('menu')
    cache.delete(f'page_{instance.slug}')

@receiver([pre_delete, pre_save], sender=Banner)
def banner_update(sender, instance, **kwargs):
    cache.delete('banners')
