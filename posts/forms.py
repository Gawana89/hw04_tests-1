from django.forms import ModelForm, Select, Textarea

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("group", "text")
        widgets = {
            "group": Select(
                attrs={
                    "placeholder": "Выбор группы",
                    "class": "form-control",
                }
            ),
            "text": Textarea(
                attrs={
                    "placeholder": "Введите текст",
                    "class": "form-control",
                }
            ),
        }
