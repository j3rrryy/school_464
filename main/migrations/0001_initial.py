# Generated by Django 4.2.1 on 2023-12-13 16:18

import django_ckeditor_5.fields
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Banner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                (
                    "banner",
                    django_resized.forms.ResizedImageField(
                        crop=None,
                        force_format="WEBP",
                        keep_meta=True,
                        quality=75,
                        scale=None,
                        size=[145, 80],
                        upload_to="",
                        verbose_name="Баннер",
                    ),
                ),
                ("url", models.CharField(max_length=255, verbose_name="Ссылка")),
                ("position", models.IntegerField(default=1, verbose_name="Позиция")),
                (
                    "is_enabled",
                    models.BooleanField(default=True, verbose_name="Включен"),
                ),
            ],
            options={
                "verbose_name": "баннер",
                "verbose_name_plural": "Баннеры",
            },
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(max_length=255, unique=True, verbose_name="URL"),
                ),
                (
                    "headline",
                    models.CharField(max_length=255, verbose_name="Заголовок"),
                ),
                ("text", django_ckeditor_5.fields.CKEditor5Field(verbose_name="Текст")),
                (
                    "photo",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=None,
                        force_format="WEBP",
                        keep_meta=True,
                        quality=75,
                        scale=None,
                        size=[640, 360],
                        upload_to="",
                        verbose_name="Фото",
                    ),
                ),
                (
                    "is_pinned",
                    models.BooleanField(default=False, verbose_name="Закреплено"),
                ),
                ("date", models.DateField(auto_now_add=True, verbose_name="Дата")),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="Опубликовано"),
                ),
            ],
            options={
                "verbose_name": "новость",
                "verbose_name_plural": "Новости",
            },
        ),
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(max_length=255, unique=True, verbose_name="URL"),
                ),
                (
                    "content",
                    django_ckeditor_5.fields.CKEditor5Field(
                        verbose_name="Содержимое страницы"
                    ),
                ),
                (
                    "in_menu",
                    models.BooleanField(default=True, verbose_name="Включен в меню"),
                ),
                (
                    "menu_info",
                    models.CharField(max_length=255, verbose_name="Имя в меню"),
                ),
                (
                    "menu_position",
                    models.IntegerField(
                        default=1, verbose_name="Позиция в меню/подменю"
                    ),
                ),
                (
                    "parent_page",
                    models.CharField(
                        choices=[("---------", "---------")],
                        default="---------",
                        max_length=255,
                        verbose_name="Имя родительского пункта в меню (если является подпунктом)",
                    ),
                ),
            ],
            options={
                "verbose_name": "страницу",
                "verbose_name_plural": "Страницы",
            },
        ),
    ]
