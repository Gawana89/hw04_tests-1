from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Group, Post
from posts.tests.test_settings import TestSettings

User = get_user_model()


class PostCreateFormTest(TestSettings):
    def test_create_new_post(self):
        """Новый пост создаётся успешно"""
        posts_count = Post.objects.count()
        group = Group.objects.get(id=1)
        form_data = {"text": "Тестовый тест(рабочий)", "group": group.id}

        response = self.authorized_client.post(
            reverse("new_post"), data=form_data, follow=True
        )
        post = Post.objects.first()
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post.text, form_data["text"])
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group.id, form_data["group"])

    def test_edit_post(self):
        """Пост редактируется"""
        form_data = {
            "text": "modified text",
            "group": self.group.id,
        }
        self.authorized_client.post(
            reverse("post_edit", args=[self.user, self.post.id]),
            data=form_data,
            follow=True,
        )
        post = Post.objects.last()
        self.assertEqual(post.text, form_data["text"])
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group.id, form_data["group"])
