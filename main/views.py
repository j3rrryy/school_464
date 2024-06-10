from typing import Any

from django.db.models import F
from django.http import Http404
from django.shortcuts import render
from django.core.cache import cache
from django.utils.html import escape
from django.db.models.query import QuerySet
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.postgres.search import SearchQuery, SearchVector

from . import models


class IndexView(TemplateView):
    """
    Main page view
    """

    template_name = "main/index.html"
    context_object_name = "index"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Школа 464"
        context["no_padding"] = True
        return context


class NewsView(ListView):
    """
    News page view with pagination
    """

    model = models.News
    template_name = "main/news.html"
    context_object_name = "news"
    paginate_by = 8

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Новости"
        context["no_padding"] = False
        return context

    def get_queryset(self) -> QuerySet[Any]:
        news = cache.get("news")

        if not news:
            news = (
                super()
                .get_queryset()
                .filter(is_published=True)
                .order_by(F("is_pinned").desc(), "-pk")
            )
            cache.set("news", news, 60 * 10)

        return news


class SearchView(ListView):
    """
    Search page view
    """

    template_name = "main/search.html"
    context_object_name = "search_results"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Поиск"
        context["no_padding"] = False
        context["query"] = self.request.GET.get("query")
        return context

    def get_queryset(self):
        query = SearchQuery(self.request.GET.get("query"))

        news_results = models.News.objects.annotate(
            search=SearchVector("headline", "text")
        )
        page_results = models.Page.objects.annotate(
            search=SearchVector("menu_info", "content")
        )

        return {
            "news": news_results.filter(search=query),
            "page": page_results.filter(search=query),
        }


class PostView(DetailView):
    """
    Post page view
    """

    model = models.News
    template_name = "main/post.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = escape(self.object.headline)  # safe header output
        context["no_padding"] = False
        return context

    def get_object(self, queryset=None) -> QuerySet[Any]:
        POST = f"post_{self.kwargs['post_slug']}"

        post = cache.get(POST)

        if not post:
            try:
                post = super().get_queryset().get(slug=self.kwargs["post_slug"])
            except:
                raise Http404()

            cache.set(POST, post, 60 * 60)

        return post


class PageView(DetailView):
    """
    Website page view
    """

    model = models.Page
    template_name = "main/page.html"
    context_object_name = "page"
    slug_url_kwarg = "page_slug"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = escape(self.object.menu_info)  # safe header output
        context["no_padding"] = False
        return context

    def get_object(self, queryset=None) -> QuerySet[Any]:
        PAGE = f"page_{self.kwargs['page_slug']}"

        page = cache.get(PAGE)

        if not page:
            try:
                page = super().get_queryset().get(slug=self.kwargs["page_slug"])
            except:
                raise Http404()

            cache.set(PAGE, page, 60 * 60)

        return page


def robots(request):
    return render(request, "system/robots.txt", content_type="text/plain")


def offline(request):
    return render(request, "system/offline.html")


def tr_handler404(request, exception):
    """
    404 error handler
    """
    return render(
        request=request,
        template_name="system/error_page.html",
        status=404,
        context={"title": "Страница не найдена: 404"},
    )


def tr_handler500(request):
    """
    500 error handler
    """
    return render(
        request=request,
        template_name="system/error_page.html",
        status=500,
        context={"title": "Ошибка сервера: 500"},
    )


def tr_handler403(request, exception):
    """
    403 error handler
    """
    return render(
        request=request,
        template_name="system/error_page.html",
        status=403,
        context={"title": "Ошибка доступа: 403"},
    )
