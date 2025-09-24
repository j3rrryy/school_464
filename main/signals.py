import os
import re

from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from . import models


@receiver(pre_save, sender=models.News)
def news_update_search_vector(sender, instance, **kwargs):
    instance.search_vector = SearchVector("headline", weight="A") + SearchVector(
        "text", weight="B"
    )


@receiver([post_save, post_delete], sender=models.News)
def news_update(sender, instance, **kwargs):
    cache.delete(f"post_{instance.slug}")


@receiver(post_delete, sender=models.News)
def news_delete(sender, instance, **kwargs):
    to_delete = re.findall(r"\"/media/other/(.+?)\"", instance.text)

    for file in to_delete:
        path = f"{settings.MEDIA_ROOT}/other/{file}"
        if os.path.exists(path):
            os.remove(path)


@receiver(pre_save, sender=models.Page)
def page_update_search_vector(sender, instance, **kwargs):
    instance.search_vector = SearchVector("name", weight="A") + SearchVector(
        "content", weight="B"
    )


@receiver([post_save, post_delete], sender=models.Page)
def page_update(sender, instance, **kwargs):
    cache.delete_many(("menu", f"page_{instance.slug}"))


@receiver(post_delete, sender=models.Page)
def page_delete(sender, instance, **kwargs):
    to_delete = re.findall(r"\"/media/other/(.+?)\"", instance.content)

    for file in to_delete:
        path = f"{settings.MEDIA_ROOT}/other/{file}"
        if os.path.exists(path):
            os.remove(path)


@receiver([post_save, post_delete], sender=models.Banner)
def banners_update(sender, instance, **kwargs):
    cache.delete("banners")
