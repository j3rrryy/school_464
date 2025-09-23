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
            slug="test-page", content="Test Content", name="Test Page"
        )

    def test_index_view(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")

    def test_news_view(self):
        response = self.client.get(reverse("news"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/news.html")

    def test_search_view(self):
        response = self.client.get(reverse("search"), {"query": "Test"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/search.html")
        self.assertContains(response, "Test News")
        self.assertContains(response, "Test Page")

    def test_post_view(self):
        response = self.client.get(
            reverse("post", kwargs={"post_slug": self.test_news.slug})
        )
        response_404 = self.client.get(
            reverse("post", kwargs={"post_slug": "does-not-exist"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/post.html")
        self.assertContains(response, "Test News")

        self.assertEqual(response_404.status_code, 404)
        self.assertTemplateUsed(response_404, "system/error_page.html")

    def test_page_view(self):
        response = self.client.get(
            reverse("page", kwargs={"page_slug": self.test_page.slug})
        )
        response_404 = self.client.get(
            reverse("page", kwargs={"page_slug": "does-not-exist"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/page.html")
        self.assertContains(response, "Test Page")

        self.assertEqual(response_404.status_code, 404)
        self.assertTemplateUsed(response_404, "system/error_page.html")

    def tearDown(self):
        self.test_news.delete()
        self.test_page.delete()


class SystemViewsTestCase(TestCase):
    def test_robots(self):
        response = self.client.get(reverse("robots"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "system/robots.txt")
        self.assertContains(response, "User-agent: *")

    def test_offline(self):
        response = self.client.get(reverse("offline"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "system/offline.html")
        self.assertContains(response, "Нет подключения к интернету")
