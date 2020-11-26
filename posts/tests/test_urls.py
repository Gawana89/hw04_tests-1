from django.urls import reverse

from posts.tests.test_settings import TestSettings


class PostURLTests(TestSettings):
    def test_accessibility_urls(self):
        """Тест работоспособности страниц"""
        patterns_and_codes = PostURLTests.patterns_and_codes
        for pattern, usertype_code in patterns_and_codes.items():
            for usertype, code in usertype_code.items():
                if usertype == "anonymous":
                    response = self.anonymous_client.get(pattern)
                else:
                    response = self.authorized_client.get(pattern)
                self.assertEqual(response.status_code, code)

    def test_accessibility_edit_post_url(self):
        """Тест страницы редактирования поста"""
        pattern = reverse(
            "post_edit", kwargs={"username": "Stevinel", "post_id": 1}
        )
        response_anonymous = self.anonymous_client.get(pattern)
        response_not_author = self.not_author.get(pattern)
        response_author = self.authorized_client.get(pattern)
        self.assertEqual(response_anonymous.status_code, 302)
        self.assertRedirects(
            response_not_author,
            reverse("post", kwargs={"username": "Stevinel", "post_id": 1}),
        )
        self.assertEqual(response_author.status_code, 200)
