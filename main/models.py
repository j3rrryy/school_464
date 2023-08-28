from datetime import date, timedelta

from django.db import models
from django.urls import reverse
from django.core.cache import cache
from django_ckeditor_5.fields import CKEditor5Field
from django_resized import ResizedImageField


class News(models.Model):
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')
    headline = models.CharField(max_length=255, verbose_name='Заголовок')
    text = CKEditor5Field(verbose_name='Текст', config_name='default')
    photo = ResizedImageField(blank=True, force_format='WEBP',
                              quality=75, verbose_name='Фото')
    is_pinned = models.BooleanField(default=False, verbose_name='Закреплено')
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    is_published = models.BooleanField(
        default=True, verbose_name='Опубликовано')

    def __str__(self) -> str:
        return str(self.headline)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('news')  # delete the cache to display new data

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete('news')  # delete the cache to display updated data

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'Новости'


class Page(models.Model):
    # page/subpage choices
    CHOICES = (
        ('menu', 'Пункт'),
        ('sub_menu', 'Подпункт')
    )

    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')
    content = CKEditor5Field(verbose_name='Содержимое страницы',
                             config_name='default')
    in_menu = models.BooleanField(default=True, verbose_name='Включен в меню')
    menu_info = models.CharField(max_length=255, verbose_name='Имя в меню')
    menu_position = models.IntegerField(
        default=1, verbose_name='Позиция в меню/подменю')
    is_subpage = models.CharField(
        max_length=255, default='menu', choices=CHOICES, verbose_name='Пункт/подпункт')
    parent_page = models.CharField(
        max_length=255, blank=True, verbose_name='Имя родительского пункта в меню')

    def __str__(self):
        return str(self.menu_info)

    def get_absolute_url(self):
        return reverse('page', kwargs={'page_slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('menu')  # delete the cache to display new data

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete('menu')  # delete the cache to display updated data

    class Meta:
        verbose_name = 'страницу'
        verbose_name_plural = 'Страницы'


class Banner(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    banner = ResizedImageField(force_format='WEBP', quality=75,
                               verbose_name='Баннер')
    url = models.CharField(max_length=255, verbose_name='Ссылка')
    position = models.IntegerField(default=1, verbose_name='Позиция')
    is_enabled = models.BooleanField(default=True, verbose_name='Включен')

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('banners')  # delete the cache to display new data

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete('banners')  # delete the cache to display updated data

    class Meta:
        verbose_name = 'баннер'
        verbose_name_plural = 'Баннеры'


class YandexDiskToken(models.Model):
    token = models.CharField(max_length=60, verbose_name='Токен Яндекс Диска')
    expiration_date = models.DateField(default=date.today() + timedelta(weeks=52),
                                       verbose_name='Дата истечения')

    def __str__(self):
        return str(self.token)

    class Meta:
        verbose_name = 'токен Яндекс Диска'
        verbose_name_plural = 'Токен Яндекс Диска'
