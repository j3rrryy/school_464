from django.urls import path
from django.contrib.sitemaps.views import sitemap

from .sitemap import *
from .views import *


sitemaps = {
    'news': NewsSitemap,
    'pages': PageSitemap
}

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('news/', NewsView.as_view(), name='news'),
    path('search/', SearchView.as_view(), name='search'),
    path('post/<slug:post_slug>/', PostView.as_view(), name='post'),
    path('<slug:page_slug>/', PageView.as_view(), name='page'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemaps'),
]
