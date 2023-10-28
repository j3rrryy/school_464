from django.contrib.syndication.views import Feed
from .models import News


class LatestNewsFeed(Feed):
    title = "Новости школы 464"
    link = "/feeds/"
    description = "Последние новости на сайте школы 464."

    def items(self):
        return News.objects.order_by('-date')[:5]

    def item_title(self, item):
        return item.headline

    def item_description(self, item):
        return item.text
