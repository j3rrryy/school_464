from django.contrib.syndication.views import Feed

from .models import News


class LatestNewsFeed(Feed):
    title = "Новости школы 464"
    link = "/news/"
    description = "Последние новости на сайте школы 464."

    def items(self):
        return News.objects.filter(is_published=True).order_by("-date")[:5]

    def item_title(self, item: News):
        return item.headline

    def item_description(self, item: News):
        return item.text
