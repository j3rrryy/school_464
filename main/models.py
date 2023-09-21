from django.db import models
from django.urls import reverse
from django.core.cache import cache
from froala_editor.fields import FroalaField
from django_resized import ResizedImageField


class News(models.Model):
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')
    headline = models.CharField(max_length=255, verbose_name='Заголовок')
    text = FroalaField(verbose_name='Текст')
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

        # delete the cache to display new data
        cache.delete('news')
        cache.delete(f'post_{self.slug}')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        # delete the cache to display new data
        cache.delete('news')
        cache.delete(f'post_{self.slug}')

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'Новости'


class Page(models.Model):
    # page/subpage choices
    TYPE_CHOICES = (
        ('menu', 'Пункт'),
        ('sub_menu', 'Подпункт')
    )

    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')
    content = FroalaField(verbose_name='Содержимое страницы')
    in_menu = models.BooleanField(default=True, verbose_name='Включен в меню')
    menu_info = models.CharField(max_length=255, verbose_name='Имя в меню')
    menu_position = models.IntegerField(
        default=1, verbose_name='Позиция в меню/подменю')
    is_subpage = models.CharField(
        max_length=255, default='menu', choices=TYPE_CHOICES, verbose_name='Пункт/подпункт')
    parent_page = models.CharField(
        max_length=255, default='blank', choices=[], verbose_name='Имя родительского пункта в меню')

    def __str__(self):
        return str(self.menu_info)

    def get_absolute_url(self):
        return reverse('page', kwargs={'page_slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # delete the cache to display new data
        cache.delete('menu')
        cache.delete(f'page_{self.slug}')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        # delete the cache to display new data
        cache.delete('menu')
        cache.delete(f'page_{self.slug}')

    def set_parent_choices(self):
        parent_choices = Page.objects.filter(in_menu=True).values_list('menu_info', 'menu_info')
        self._meta.get_field('parent_page').choices = [('blank', '---------')] + list(parent_choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_parent_choices()

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
