import math
from collections import OrderedDict

from django.core.cache import cache

from .models import *


def menu_data(request):
    """
    Create a menu with sub-items.
    """

    MENU = 'menu'

    menu = cache.get(MENU)

    if not menu:
        data = Page.objects.filter(in_menu=True)
        menu = OrderedDict()

        for item in sorted(filter(lambda x: x.is_subpage == 'menu', data), key=lambda y: y.menu_position):
            menu[item] = []  # create base menu items

        for item in sorted(filter(lambda x: x.is_subpage == 'sub_menu', data), key=lambda y: y.menu_position):
            parent_item = next(
                (x for x in data if x.menu_info == item.parent_page), None)
            if parent_item:
                menu[parent_item].append(item)  # create sub menu items

        cache.set(MENU, menu, 60 * 60)

    return {MENU: menu.items()}


def banners_data(request):
    """
    Create table with banners.
    """

    BANNERS = 'banners'

    banners = cache.get(BANNERS)

    if not banners:
        banners_list = sorted(Banner.objects.filter(
            is_enabled=True), key=lambda banner: banner.position)
        banners = [[] for _ in range(math.ceil(len(banners_list) / 4))]
        i = 0  # position of list in res
        c = 0  # amount of banners in this list

        for banner in banners_list:
            banners[i].append(banner)
            c += 1
            if c == 4:  # max 4 banners in each row
                i += 1
                c = 0

        cache.set(BANNERS, banners, 60 * 60)

    return {BANNERS: banners}
