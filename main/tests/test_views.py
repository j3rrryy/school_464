from django.test import TestCase
from django.urls import reverse

from main.models import News, Page


class MainViewsTestCase(TestCase):
    def setUp(self):
        self.test_news = News.objects.create(
            slug="test-news",
            headline="Test News",
            text="Test Text",
            is_published=True,
            is_pinned=True,
        )

        self.test_page = Page.objects.create(
            slug="test-page", content="Test Content", menu_info="Test Page"
        )

    def test_IndexView(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")

    def test_NewsView(self):
        response = self.client.get(reverse("news"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/news.html")

    def test_SearchView(self):
        response = self.client.get(reverse("search"), {"query": "Test"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/search.html")
        self.assertContains(response, "Test News")
        self.assertContains(response, "Test Page")

    def test_PostView(self):
        response = self.client.get(
            reverse("post", kwargs={"post_slug": self.test_news.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/post.html")
        self.assertContains(response, "Test News")

    def test_PageView(self):
        response = self.client.get(
            reverse("page", kwargs={"page_slug": self.test_page.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/page.html")
        self.assertContains(response, "Test Page")


class SystemViewsTestCase(TestCase):
    def test_offline(self):
        response = self.client.get(reverse("offline"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "system/offline.html")
        self.assertContains(response, "Нет подключения к интернету")
