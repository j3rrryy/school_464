from django.urls import reverse
from django.test import TestCase

from main.models import News, Page


class MainSitemapsTestCase(TestCase):
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

    def test_sitemaps(self):
        response = self.client.get(reverse("sitemaps"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            reverse("post", kwargs={"post_slug": self.test_news.slug}) + "</loc>",
        )
        self.assertContains(
            response,
            reverse("page", kwargs={"page_slug": self.test_page.slug}) + "</loc>",
        )

    def tearDown(self):
        self.test_news.delete()
        self.test_page.delete()
