import os
import re

from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.News)
def news_update_search_vector(sender, instance, **kwargs):
    models.News.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector("headline", weight="A")
        + SearchVector("text", weight="B")
    )


@receiver([post_save, post_delete], sender=models.News)
def news_update(sender, instance, **kwargs):
    cache.delete(f"post_{instance.slug}")


@receiver(post_delete, sender=models.News)
def news_delete(sender, instance, **kwargs):
    to_delete = re.findall(rf"\"{settings.MEDIA_URL}other/(.+?)\"", instance.text)

    for file in to_delete:
        path = f"{settings.MEDIA_ROOT}/other/{file}"
        if os.path.exists(path):
            os.remove(path)


@receiver(post_save, sender=models.Page)
def page_update_search_vector(sender, instance, **kwargs):
    models.Page.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector("name", weight="A")
        + SearchVector("content", weight="B")
    )


@receiver([post_save, post_delete], sender=models.Page)
def page_update(sender, instance, **kwargs):
    cache.delete_many(("menu", f"page_{instance.slug}"))


@receiver(post_delete, sender=models.Page)
def page_delete(sender, instance, **kwargs):
    to_delete = re.findall(rf"\"{settings.MEDIA_URL}other/(.+?)\"", instance.content)

    for file in to_delete:
        path = f"{settings.MEDIA_ROOT}/other/{file}"
        if os.path.exists(path):
            os.remove(path)


@receiver([post_save, post_delete], sender=models.Banner)
def banners_update(sender, instance, **kwargs):
    cache.delete("banners")
