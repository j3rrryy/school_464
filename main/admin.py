from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


def make_published(modeladmin, request, queryset):
    """
    Publish the news.
    """

    queryset.update(is_published=True)


make_published.short_description = "Опубликовать выбранные новости"


def make_unpublished(modeladmin, request, queryset):
    """
    Unpublish the news.
    """

    queryset.update(is_published=False)


make_unpublished.short_description = "Снять выбранные новости"


def pin(modeladmin, request, queryset):
    """
    Pin the news.
    """

    queryset.update(is_pinned=True)


pin.short_description = "Закрепить"


def unpin(modeladmin, request, queryset):
    """
    Unpin the news.
    """

    queryset.update(is_pinned=False)


unpin.short_description = "Открепить"


def enable_item(modeladmin, request, queryset):
    """
    Enable the page in the menu.
    """

    queryset.update(in_menu=True)


enable_item.short_description = "Включить в меню"


def disable_item(modeladmin, request, queryset):
    """
    Remove the page from the menu.
    """

    queryset.update(in_menu=False)


disable_item.short_description = "Убрать из меню"


def enable_banner(modeladmin, request, queryset):
    """
    Enable banner.
    """

    queryset.update(is_enabled=True)


enable_banner.short_description = "Включить"


def disable_banner(modeladmin, request, queryset):
    """
    Disable banner.
    """

    queryset.update(is_enabled=False)


disable_banner.short_description = "Выключить"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'headline', 'get_photo',
                    'is_pinned', 'date', 'is_published')
    list_display_links = ('id', 'slug', 'headline')
    search_fields = ('headline', 'text', 'date')
    prepopulated_fields = {'slug': ('headline',)}
    fields = ('headline', 'slug', 'text', 'photo',
              'get_photo', 'is_pinned', 'is_published')
    readonly_fields = ('get_photo', )
    actions = [make_published, make_unpublished, pin, unpin]

    def get_photo(self, object):
        if object.photo:
            # get preview
            return mark_safe(f"<img src='{object.photo.url}' width=100>")

    get_photo.short_description = "Миниатюра"


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'in_menu', 'menu_info',
                    'menu_position', 'is_subpage', 'parent_page')
    list_display_links = ('id', 'slug')
    search_fields = ('id', 'content', 'menu_info',
                     'menu_position', 'in_menu', 'parent_page')
    fields = ('menu_info', 'slug', 'content', 'in_menu',
              'is_subpage', 'parent_page', 'menu_position')
    prepopulated_fields = {'slug': ('menu_info',)}
    actions = [enable_item, disable_item]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_banner',
                    'url', 'position', 'is_enabled')
    list_display_links = ('id', 'name', 'get_banner', 'url')
    search_fields = ('id', 'name', 'url', 'position')
    fields = ('name', 'url', 'banner', 'get_banner', 'position', 'is_enabled')
    readonly_fields = ('get_banner', )
    actions = [enable_banner, disable_banner]

    def get_banner(self, object):
        if object.banner:
            # get preview
            return mark_safe(f"<img src='{object.banner.url}' width=100>")

    get_banner.short_description = "Миниатюра"
