from django.urls import path
from django.contrib.sitemaps.views import sitemap

from . import views
from . import sitemap as sitemaps


sitemaps = {
    'news': sitemaps.NewsSitemap,
    'pages': sitemaps.PageSitemap
}

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('post/<slug:post_slug>/', views.PostView.as_view(), name='post'),
    path('<slug:page_slug>/', views.PageView.as_view(), name='page'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemaps'),
]
