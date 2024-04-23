import os
import re

from django.conf import settings
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save

from . import models


@receiver([pre_delete, pre_save], sender=models.News)
def news_update(sender, instance, **kwargs):
    cache.delete("news")
    cache.delete(f"post_{instance.slug}")


@receiver(pre_delete, sender=models.News)
def news_delete(sender, instance, **kwargs):
    to_delete = re.findall(r"\"/media/other/(.+?)\"", instance.text)

    for file in to_delete:
        path = f"{settings.MEDIA_ROOT}/other/{file}"
        if os.path.exists(path):
            os.remove(path)


@receiver([pre_delete, pre_save], sender=models.Page)
def page_update(sender, instance, **kwargs):
    cache.delete("menu")
    cache.delete(f"page_{instance.slug}")


@receiver(pre_delete, sender=models.Page)
def page_delete(sender, instance, **kwargs):
    to_delete = re.findall(r"\"/media/other/(.+?)\"", instance.content)

    for file in to_delete:
        path = f"{settings.MEDIA_ROOT}/other/{file}"
        if os.path.exists(path):
            os.remove(path)


@receiver([pre_delete, pre_save], sender=models.Banner)
def banner_update(sender, instance, **kwargs):
    cache.delete("banners")
