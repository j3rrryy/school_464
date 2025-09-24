from typing import Any

from django.contrib.postgres.search import SearchQuery, SearchRank
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import render
from django.utils.html import escape
from django.views.generic import DetailView, ListView, TemplateView

from . import models


class IndexView(TemplateView):
    template_name = "main/index.html"
    context_object_name = "index"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Школа 464"
        context["no_padding"] = True
        return context


class NewsView(ListView):
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
        return (
            super()
            .get_queryset()
            .filter(is_published=True)
            .order_by(F("is_pinned").desc(), "-pk")
        )


class SearchView(ListView):
    template_name = "main/search.html"
    context_object_name = "search_results"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Поиск"
        context["no_padding"] = False
        context["query"] = self.request.GET.get("query")
        return context

    def get_queryset(self):
        query = SearchQuery(self.request.GET.get("query", ""))

        news_results = (
            models.News.objects.annotate(
                rank=SearchRank(F("search_vector"), query, cover_density=True)
            )
            .filter(search_vector=query)
            .order_by("-rank")[:15]
        )
        page_results = (
            models.Page.objects.annotate(
                rank=SearchRank(F("search_vector"), query, cover_density=True)
            )
            .filter(search_vector=query)
            .order_by("-rank")[:15]
        )

        return {"news": news_results, "page": page_results}


class PostView(DetailView):
    model = models.News
    template_name = "main/post.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = escape(self.object.headline)
        context["no_padding"] = False
        return context

    def get_object(self, queryset=None) -> QuerySet[Any]:
        cache_key = f"post_{self.kwargs['post_slug']}"
        post = cache.get(cache_key)

        if not post:
            try:
                post = super().get_queryset().get(slug=self.kwargs["post_slug"])
            except ObjectDoesNotExist:
                raise Http404()
            cache.set(cache_key, post)

        return post


class PageView(DetailView):
    model = models.Page
    template_name = "main/page.html"
    context_object_name = "page"
    slug_url_kwarg = "page_slug"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = escape(self.object.name)
        context["no_padding"] = False
        return context

    def get_object(self, queryset=None) -> QuerySet[Any]:
        cache_key = f"page_{self.kwargs['page_slug']}"
        page = cache.get(cache_key)

        if not page:
            try:
                page = super().get_queryset().get(slug=self.kwargs["page_slug"])
            except ObjectDoesNotExist:
                raise Http404()
            cache.set(cache_key, page)

        return page


def robots(request):
    return render(request, "system/robots.txt", content_type="text/plain")


def offline(request):
    return render(request, "system/offline.html")


def tr_handler404(request, exception):
    return render(
        request=request,
        template_name="system/error_page.html",
        status=404,
        context={"title": "Страница не найдена: 404"},
    )


def tr_handler500(request):
    return render(
        request=request,
        template_name="system/error_page.html",
        status=500,
        context={"title": "Ошибка сервера: 500"},
    )


def tr_handler403(request, exception):
    return render(
        request=request,
        template_name="system/error_page.html",
        status=403,
        context={"title": "Ошибка доступа: 403"},
    )
