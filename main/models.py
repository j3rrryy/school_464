from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField
from django_ckeditor_5.fields import CKEditor5Field


class News(models.Model):
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )
    headline = models.CharField(max_length=255, verbose_name="Заголовок")
    text = CKEditor5Field(verbose_name="Текст")
    photo = ResizedImageField(
        blank=True,
        force_format="WEBP",
        upload_to="news/",
        size=[640, 360],
        quality=75,
        verbose_name="Фото",
    )
    is_pinned = models.BooleanField(default=False, verbose_name="Закреплено")
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    def __str__(self) -> str:
        return str(self.headline)

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "Новости"


class Page(models.Model):
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )
    content = CKEditor5Field(verbose_name="Содержимое страницы")
    in_menu = models.BooleanField(default=True, verbose_name="Включен в меню")
    menu_info = models.CharField(max_length=255, verbose_name="Имя в меню")
    menu_position = models.IntegerField(
        default=1, verbose_name="Позиция в меню/подменю"
    )
    parent_page = models.CharField(
        max_length=255,
        default="---------",
        choices=[("---------", "---------")],
        verbose_name="Имя родительского пункта в меню (если является подпунктом)",
    )

    def __str__(self):
        return str(self.menu_info)

    def get_absolute_url(self):
        return reverse("page", kwargs={"page_slug": self.slug})

    def set_parent_choices(self):
        parent_choices = Page.objects.filter(
            in_menu=True, parent_page="---------"
        ).values_list("menu_info", "menu_info")
        self._meta.get_field("parent_page").choices = [
            ("---------", "---------")
        ] + list(parent_choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_parent_choices()

    class Meta:
        verbose_name = "страницу"
        verbose_name_plural = "Страницы"


class Banner(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    banner = ResizedImageField(
        force_format="WEBP",
        upload_to="banners/",
        size=[145, 80],
        quality=75,
        verbose_name="Баннер",
    )
    url = models.CharField(max_length=255, verbose_name="Ссылка")
    position = models.IntegerField(default=1, verbose_name="Позиция")
    is_enabled = models.BooleanField(default=True, verbose_name="Включен")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "баннер"
        verbose_name_plural = "Баннеры"
