from django.core.cache import cache
from django.db.models import Prefetch

from . import models


def menu_data(request):
    menu = cache.get("menu")

    if not menu:
        children_qs = models.Page.objects.filter(in_menu=True).order_by("menu_position")
        root_pages = (
            models.Page.objects.filter(in_menu=True, parent__isnull=True)
            .prefetch_related(Prefetch("children", queryset=children_qs))
            .order_by("menu_position", "name")
        )

        menu = {root: tuple(root.children.all()) for root in root_pages}
        cache.set("menu", menu, None)

    return {"menu": menu.items()}


def banners_data(request):
    banners = cache.get("banners")

    if not banners:
        banner_list = models.Banner.objects.filter(is_enabled=True).order_by("position")
        banners = [banner_list[i : i + 4] for i in range(0, len(banner_list), 4)]
        cache.set("banners", banners, None)

    return {"banners": banners}
