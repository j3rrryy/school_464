from django.contrib.sitemaps import Sitemap

from .models import News, Page


class NewsSitemap(Sitemap):
    """
    Sitemap for news
    """

    changefreq = 'never'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return News.objects.all()

    def lastmod(self, obj):
        return obj.date


class PageSitemap(Sitemap):
    """
    Sitemap for pages
    """

    changefreq = 'monthly'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Page.objects.all()
