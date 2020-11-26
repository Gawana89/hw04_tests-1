from django import forms
from django.urls import reverse

from posts.tests.test_settings import TestSettings


class PostPagesTests(TestSettings):
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            reverse("index"): "index.html",
            reverse("group", kwargs={"slug": "test-group"}): "group.html",
            reverse("new_post"): "new.html",
            reverse(
                "post_edit", kwargs={"username": "Stevinel", "post_id": 1}
            ): "new.html",
        }

        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("index"))
        self.assertIn("page", response.context)
        self.assertEqual(
            len(response.context["paginator"].page(1).object_list), 10
        )

    def test_group_page_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("group", kwargs={"slug": "test-group"})
        )
        self.assertEqual(response.context["group"], self.group)
        self.assertIn("page", response.context)
        self.assertEqual(
            len(response.context["paginator"].page(1).object_list), 10
        )

    def test_new_page_show_correct_context(self):
        """Шаблон new сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("new_post"))
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for name, expected in form_fields.items():
            with self.subTest(name=name):
                field_filled = response.context.get("form").fields.get(name)
                self.assertIsInstance(field_filled, expected)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""

        response = self.authorized_client.get(
            reverse("profile", kwargs={"username": "Stevinel"})
        )
        self.assertEqual(response.context["user_profile"], self.user)
        self.assertEqual(response.context["username"], "Stevinel")
        self.assertEqual(response.context["post_count"], 14)
        self.assertIn("page", response.context)
        self.assertEqual(
            len(response.context["paginator"].page(2).object_list), 4
        )

    def test_post_page_show_correct_context(self):
        """Шаблон post сформирован с правильным контекстом."""

        response = self.authorized_client.get(
            reverse("post", kwargs={"username": "Stevinel", "post_id": 1})
        )
        self.assertEqual(response.context["user_profile"], self.user)
        self.assertEqual(response.context["post"], self.post)
        self.assertEqual(response.context["username"], "Stevinel")
        self.assertEqual(response.context["post_count"], 14)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""

        response = self.authorized_client.get(
            reverse("post_edit", kwargs={"username": "Stevinel", "post_id": 1})
        )
        self.assertIn("form", response.context)
        self.assertEqual(response.context["post"], self.post)

    def test_flatpages_show_correct_status_code(self):
        """Шаблоны flatpages возвращают ответ с правильным кодом статуса."""

        for url in self.static_pages:
            response = self.anonymous_client.get(url)
            with self.subTest():
                self.assertEqual(response.status_code, 200)

    def test_new_post_in_correct_group(self):
        """Пост находится в правильной группе"""

        group_posts_pk = self.group.posts.values_list("id", flat=True)
        group2_posts_pk = self.group2.posts.values_list("id", flat=True)
        self.assertIn(self.post.id, group_posts_pk)
        self.assertNotIn(self.post.id, group2_posts_pk)
