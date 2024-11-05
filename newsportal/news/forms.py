from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # Указываем, что форма основана на модели Post
        fields = ['title', 'text', 'author']  # Поля, которые будут доступны в форме (без поля type)
