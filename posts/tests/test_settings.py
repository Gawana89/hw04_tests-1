from django.contrib.auth import get_user_model
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class TestSettings(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создание объектов.

        Объекты будут импортироваться в другие тесты"""
        super().setUpClass()
        cls.user = User.objects.create(
            id=1,
            username="Stevinel",
            first_name="Stan",
            last_name="Voronov",
        )
        cls.group = Group.objects.create(
            id=1,
            title="test",
            slug="test-group",
            description="some description",
        )
        cls.group2 = Group.objects.create(
            title="test2", slug="test-group2", description="some description2"
        )
        cls.user_not_author = User.objects.create(username="NotAuthor")

        Post.objects.create(
            id=1,
            author=cls.user,
            text="Тестовый тест(рабочий)",
            group=cls.group,
        )
        Post.objects.create(
            id=2,
            text="Some text",
            author=cls.user,
            group=cls.group2,
        )

        cls.post = Post.objects.get(id=1)

        cls.patterns_and_codes = {
            reverse("index"): {"anonymous": 200, "authorized": 200},
            reverse("group", kwargs={"slug": "test-group"}): {
                "anonymous": 200,
                "authorized": 200,
            },
            reverse("new_post"): {"anonymous": 302, "authorized": 200},
            reverse("profile", kwargs={"username": "Stevinel"}): {
                "anonymous": 200,
                "authorized": 200,
            },
            reverse("post", kwargs={"username": "Stevinel", "post_id": 1}): {
                "anonymous": 200,
                "authorized": 200,
            },
        }
        for number in range(3, 14):
            Post.objects.create(
                id=number, text="Some text", author=cls.user, group=cls.group
            )
        Post.objects.create(
            id=14, text="Some text", author=cls.user, group=cls.group2
        )

        site = Site.objects.get(id=1)
        flat_about = FlatPage.objects.create(
            url="/about-author/",
            title="about me",
            content="<b>some content</b>",
        )
        flat_tech = FlatPage.objects.create(
            url="/about-spec/",
            title="about my tech",
            content="<b>some content</b>",
        )
        flat_about.sites.add(site)
        flat_tech.sites.add(site)
        cls.static_pages = ("/about-author/", "/about-spec/")

    def setUp(self):
        super().setUp()
        self.anonymous_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.not_author = Client()
        self.not_author.force_login(self.user_not_author)
