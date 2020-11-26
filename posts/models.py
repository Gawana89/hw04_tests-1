from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        verbose_name="Введите текст",
        help_text="Введите текст вашего будущего поста",
    )
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    group = models.ForeignKey(
        "Group",
        verbose_name="Выберите группу",
        help_text="Выберите группу из существующих",
        related_name="posts",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Название группы",
    )
    slug = models.SlugField(
        max_length=256,
        unique=True,
        verbose_name="Слаг",
        help_text="Адрес для страницы с группой",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Описание группы"
    )

    def __str__(self):
        return self.title
