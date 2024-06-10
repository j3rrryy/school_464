from django.urls import reverse
from django.test import TestCase

from main.models import News


class MainRSSTestCase(TestCase):
    def setUp(self):
        self.test_news = News.objects.create(
            slug="test-news",
            headline="Test News",
            text="Test Text",
            is_published=True,
            is_pinned=True,
        )

    def test_rss(self):
        response = self.client.get(reverse("feed"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, f"<title>{self.test_news.headline}</title>")
        self.assertContains(
            response, f"<description>{self.test_news.text}</description>"
        )
        self.assertContains(
            response,
            reverse("post", kwargs={"post_slug": self.test_news.slug}) + "</link>",
        )

    def tearDown(self):
        self.test_news.delete()
