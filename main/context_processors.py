import math

from django.core.cache import cache

from . import models


def menu_data(request):
    """
    Create a menu with sub-items.
    """

    menu = cache.get("menu")

    if not menu:
        data = models.Page.objects.filter(in_menu=True)
        menu = {}

        for item in sorted(
            filter(lambda x: x.parent_page == "---------", data),
            key=lambda y: y.menu_position,
        ):
            menu[item] = []  # create base menu items

        for item in sorted(
            filter(lambda x: x.parent_page != "---------", data),
            key=lambda y: y.menu_position,
        ):
            parent_item = next(
                (x for x in data if x.menu_info == item.parent_page), None
            )
            if parent_item:
                menu[parent_item].append(item)  # create sub menu items

        cache.set("menu", menu, 60 * 60)

    return {"menu": menu.items()}


def banners_data(request):
    """
    Create table with banners.
    """

    banners = cache.get("banners")

    if not banners:
        banners_list = sorted(
            models.Banner.objects.filter(is_enabled=True),
            key=lambda banner: banner.position,
        )
        banners = [[] for _ in range(math.ceil(len(banners_list) / 4))]
        i = 0  # position of list in res
        c = 0  # amount of banners in this list

        for banner in banners_list:
            banners[i].append(banner)
            c += 1
            if c == 4:  # max 4 banners in each row
                i += 1
                c = 0

        cache.set("banners", banners, 60 * 60)

    return {"banners": banners}
