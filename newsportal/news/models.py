from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    name = models.CharField(max_length=100, null=True)
    def update_rating(self):
        # Суммарный рейтинг постов автора * 3
        post_rating = sum(post.rating * 3 for post in self.post_set.all())

        # Суммарный рейтинг комментариев, оставленных автором
        comment_ratings = sum(comment.rating for comment in self.user.comment_set.all())

        # Суммарный рейтинг комментариев к постам автора
        post_comment_rating = sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())

        # Итоговый рейтинг
        self.rating = post_rating + comment_ratings + post_comment_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)


class Post(models.Model):
    # Определяем возможные типы новостей
    TYPE_CHOICES = [
        ('article', 'Article'),  # Тип 'статья'
        ('news', 'News'),     # Тип 'новость'
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)  # Автор новости
    post_type = models.CharField(max_length=10, choices=[('articles', 'Article'), ('news', 'News')], null=True)
    created_at = models.DateTimeField(auto_now_add=True)    # Дата публикации
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200, null=True)  # Заголовок новости
    rating = models.IntegerField(default=0, null=True)
    text = models.TextField(null=True)  # Добавляем поле для текста поста

    def get_absolute_url(self):
        return reverse('news_list')  #  имя  URL для перехода после создания новости

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='text')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True)

    def like(self):
        pass

    def dislike(self):
        pass
