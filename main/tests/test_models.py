from django.test import TestCase
from django.urls import reverse

from main.models import Banner, News, Page


class MainNewsModelTestCase(TestCase):
    def setUp(self):
        self.test_news = News.objects.create(
            slug="test-news", headline="Test News", text="Test Text"
        )

    def test_is_pinned_false_by_default(self):
        """
        Test that the news aren't pinned by default.
        """

        self.assertTrue(isinstance(self.test_news.is_pinned, bool))
        self.assertFalse(self.test_news.is_pinned)

    def test_is_published_true_by_default(self):
        """
        Test that that the news are published by default.
        """

        self.assertTrue(isinstance(self.test_news.is_published, bool))
        self.assertTrue(self.test_news.is_published)

    def test_str(self):
        """
        Test the __str__ method
        """

        expected = "Test News"
        actual = str(self.test_news)

        self.assertEqual(expected, actual)

    def test_get_absolute_url(self):
        """
        Test that get_absolute_url returns the expected URL.
        """

        expected = reverse("post", kwargs={"post_slug": self.test_news.slug})
        actual = self.test_news.get_absolute_url()

        self.assertEqual(expected, actual)

    def tearDown(self):
        self.test_news.delete()


class MainPageModelTestCase(TestCase):
    def setUp(self):
        self.test_page = Page.objects.create(
            slug="test-page", content="Test Content", menu_info="Test Page"
        )

    def test_menu_position_1_by_default(self):
        """
        Test that the page is on top by default.
        """

        self.assertTrue(isinstance(self.test_page.menu_position, int))
        self.assertEqual(self.test_page.menu_position, 1)

    def test_str(self):
        """
        Test the __str__ method
        """

        expected = "Test Page"
        actual = str(self.test_page)

        self.assertEqual(expected, actual)

    def test_get_absolute_url(self):
        """
        Test that get_absolute_url returns the expected URL.
        """

        expected = reverse("page", kwargs={"page_slug": self.test_page.slug})
        actual = self.test_page.get_absolute_url()

        self.assertEqual(expected, actual)

    def tearDown(self):
        self.test_page.delete()


class MainBannerModelTestCase(TestCase):
    def setUp(self):
        self.test_banner = Banner.objects.create(
            name="Test Banner", banner="/media/test.webp", url="test.com"
        )

    def test_position_1_by_default(self):
        """
        Test that the banner position is 1 by default.
        """

        self.assertTrue(isinstance(self.test_banner.position, int))
        self.assertEqual(self.test_banner.position, 1)

    def test_is_enabled_by_default(self):
        """
        Test that the banner is enabled by default.
        """

        self.assertTrue(isinstance(self.test_banner.is_enabled, bool))
        self.assertTrue(self.test_banner.position)

    def test_str(self):
        """
        Test the __str__ method
        """

        expected = "Test Banner"
        actual = str(self.test_banner)

        self.assertEqual(expected, actual)

    def tearDown(self):
        self.test_banner.delete()
