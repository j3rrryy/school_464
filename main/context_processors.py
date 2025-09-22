from django.core.cache import cache

from . import models


def menu_data(request):
    menu = cache.get("menu")

    if not menu:
        data = models.Page.objects.filter(in_menu=True).order_by("menu_position")
        menu = {}
        parents_dict = {}

        for item in data:
            if item.parent_page == "---------":
                menu[item] = []
                parents_dict[item.menu_info] = item

        for item in data:
            if item.parent_page != "---------":
                parent_item = parents_dict.get(item.parent_page)
                if parent_item:
                    menu[parent_item].append(item)

        cache.set("menu", menu, None)

    return {"menu": menu.items()}


def banners_data(request):
    banners = cache.get("banners")

    if not banners:
        banners_list = models.Banner.objects.filter(is_enabled=True).order_by(
            "position"
        )
        banners = [banners_list[i : i + 4] for i in range(0, len(banners_list), 4)]
        cache.set("banners", banners, None)

    return {"banners": banners}
