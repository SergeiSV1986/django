from django.shortcuts import render
"""
# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView
from .models import Author, Category, Post, PostCategory, Comment

class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'default.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'postss'
"""
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import PostForm


class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'  # Укажите путь к вашему шаблону
    context_object_name = 'news_list'  # Имя переменной, которая будет доступна в шаблоне
    paginate_by = 10  # Количество новостей на странице

    def get_queryset(self):
        return Post.objects.filter(post_type='news').order_by('-created_at')  # Фильтруем только новости


class NewsSearchView(ListView):
    model = Post
    template_name = 'news/news_search.html'  # Укажите путь к вашему шаблону
    context_object_name = 'news_search'        # Имя переменной, которая будет доступна в шаблоне
    paginate_by = 10  # Количество новостей на странице

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='news')
        title = self.request.GET.get('title')
        author = self.request.GET.get('author')
        date = self.request.GET.get('date')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__name__icontains=author)
        if date:
            queryset = queryset.filter(created_at__date=date)

        return queryset.order_by('-created_at')


def news_detail(request, news_id):
    post = get_object_or_404(Post, id=news_id)
    return render(request, 'news_detail.html', {'post': post})




class NewsCreate(CreateView):
    form_class = PostForm  # Указываем форму, которая будет использоваться для создания новостей
    model = Post  # Указываем модель, с которой будет работать представление
    template_name = 'news/news_form.html'  # Шаблон для создания/редактирования новостей

    def form_valid(self, form):
        # Переопределяем метод для установки типа новости перед сохранением
        news = form.save(commit=False)  # Получаем инстанс модели без сохранения в базе
        news.type = 'news'  # Устанавливаем тип как 'новость'
        return super().form_valid(form)  # Вызываем стандартный механизм сохранения


class NewsUpdate(UpdateView):
    form_class = PostForm  # Указываем форму для редактирования
    model = Post  # Указываем модель
    template_name = 'news/news_form.html'  # Шаблон для редактирования новостей


class NewsDelete(DeleteView):
    model = Post  # Указываем модель для удаления
    template_name = 'news/news_confirm_delete.html'  # Шаблон подтверждения удаления
    success_url = reverse_lazy('news_list')  # URL для перенаправления после успешного удаления


# Аналогично создаем представления для статей
class ArticleCreate(CreateView):
    form_class = PostForm  # Указываем форму для создания статей
    model = Post  # Указываем модель
    template_name = 'news/article_form.html'  # Шаблон для создания статей

    def form_valid(self, form):
        # Переопределяем метод для установки типа статьи перед сохранением
        article = form.save(commit=False)  # Получаем инстанс модели без сохранения в базе
        article.type = 'article'  # Устанавливаем тип как 'статья'
        return super().form_valid(form)  # Вызываем стандартный механизм сохранения


class ArticleUpdate(UpdateView):
    form_class = PostForm  # Указываем форму для редактирования статей
    model = Post  # Указываем модель
    template_name = 'news/article_form.html'  # Шаблон для редактирования статей


class ArticleDelete(DeleteView):
    model = Post  # Указываем модель для удаления
    template_name = 'news/article_confirm_delete.html'  # Шаблон подтверждения удаления
    success_url = reverse_lazy('article_list')  # URL для перенаправления после успешного удаления