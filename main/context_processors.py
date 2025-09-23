from django.core.cache import cache

from . import models


def menu_data(request):
    menu = cache.get("menu")

    if not menu:
        page_list = models.Page.objects.filter(in_menu=True).order_by("menu_position")
        menu = {}
        parents_dict = {}

        for page in page_list:
            if page.parent_page == "---------":
                menu[page] = []
                parents_dict[page.menu_info] = page

        for page in page_list:
            if page.parent_page != "---------":
                parent_item = parents_dict.get(page.parent_page)
                if parent_item:
                    menu[parent_item].append(page)

        cache.set("menu", menu, None)

    return {"menu": menu.items()}


def banners_data(request):
    banners = cache.get("banners")

    if not banners:
        banner_list = models.Banner.objects.filter(is_enabled=True).order_by("position")
        banners = [banner_list[i : i + 4] for i in range(0, len(banner_list), 4)]
        cache.set("banners", banners, None)

    return {"banners": banners}
