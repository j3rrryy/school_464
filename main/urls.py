from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import feeds, views
from . import sitemap as sitemaps

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("news/", views.NewsView.as_view(), name="news"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("post/<slug:post_slug>/", views.PostView.as_view(), name="post"),
    path("feed/", feeds.LatestNewsFeed(), name="feed"),
    path("offline/", views.offline, name="offline"),
    path("<slug:page_slug>/", views.PageView.as_view(), name="page"),
    path("robots.txt", views.robots, name="robots"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"news": sitemaps.NewsSitemap, "pages": sitemaps.PageSitemap}},
        name="sitemaps",
    ),
]
