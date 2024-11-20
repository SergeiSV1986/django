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
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from .forms import PostForm
from .templatetags.filters import PostFilter


class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'  # Укажите путь к вашему шаблону
    context_object_name = 'news_list'  # Имя переменной, которая будет доступна в шаблоне
    paginate_by = 3   # Количество новостей на странице

    def get_queryset(self):
        return Post.objects.filter(post_type='news').order_by('-created_at')  # Фильтруем только новости и сортируем по дате создания


class NewsSearchView(ListView):
    model = Post
    template_name = 'news/news_search.html'  # Укажите путь к вашему шаблону
    context_object_name = 'news_search'        # Имя переменной, которая будет доступна в шаблоне
    paginate_by = 2  # Количество новостей на странице

    # Переопределяем функцию получения списка статей
    def get_queryset(self):
        # Получаем обычный запрос и применяем фильтрацию
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список статей
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_search'] = self.filterset.qs  # Передаем отфильтрованные посты в контекст
        context['filterset'] = self.filterset  # Добавляем в контекст объект фильтрации.
        return context


def news_detail(request, news_id):  # Представление для отображения деталей поста
    post = get_object_or_404(Post, id=news_id)  # Получаем пост по его ID или возвращаем 404, если не найден
    return render(request, 'news_detail.html', {'post': post})  # Отображаем шаблон с деталями поста, передавая пост в контекст


class NewsCreate(CreateView):
    form_class = PostForm  # Указываем форму, которая будет использоваться для создания новостей
    model = Post  # Указываем модель, с которой будет работать представление
    template_name = 'news/news_form.html'  # Шаблон для создания/редактирования новостей
    context_object_name = 'news_create'  # Имя переменной, которая будет доступна в шаблоне

    def form_valid(self, form):
        # Переопределяем метод для установки типа новости перед сохранением
        news = form.save(commit=False)  # Получаем инстанс модели без сохранения в базе
        #news.post_type = self.kwargs.get('post_type')  # Получаем тип из URL
        news.post_type = 'news'  # Устанавливаем тип как 'новость'
        return super().form_valid(form)  # Вызываем стандартный механизм сохранения

    def get_success_url(self):
        return reverse_lazy('news_list')  # Перенаправление на список новостей

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='news')
        title = self.request.GET.get('title')
        created_at = self.request.GET.get('created_at')
        date = self.request.GET.get('date')


# Cоздаем представления для статей
class ArticleCreate(CreateView):
    form_class = PostForm  # Указываем форму для создания статей
    model = Post  # Указываем модель
    template_name = 'news/article_form.html'  # Шаблон для создания статей

    def form_valid(self, form):
        # Переопределяем метод для установки типа статьи перед сохранением
        article = form.save(commit=False)  # Получаем инстанс модели без сохранения в базе
        article.post_type = 'article'  # Устанавливаем тип как 'статья'
        return super().form_valid(form)  # Вызываем стандартный механизм сохранения

    def get_success_url(self):
        # Перенаправляем на список новостей или статей в зависимости от типа поста
        return reverse_lazy('news_list' if self.kwargs.get('post_type') == 'news' else 'news_search')


class ArticleUpdate(UpdateView):
    form_class = PostForm  # Указываем форму для редактирования статей
    model = Post  # Указываем модель
    template_name = 'news/article_form.html'  # Шаблон для редактирования статей

    def form_valid(self, form):
        post = form.save(commit=False)  # Получаем инстанс модели без сохранения в базе
        post.post_type = self.kwargs.get('post_type')  # Устанавливаем тип поста из URL
        return super().form_valid(form)  # Сохраняем изменения

    def get_success_url(self):
        # Перенаправляем на список новостей или статей в зависимости от типа поста
        return reverse_lazy('news_list' if self.object.post_type == 'news' else 'news_search')


class ArticleDelete(DeleteView):
    model = Post  # Указываем модель для удаления
    template_name = 'news/news_confirm_delete.html'  # Шаблон подтверждения удаления
    success_url = reverse_lazy('news_list')  # URL для перенаправления после успешного удаления

    def get_success_url(self):
        # Перенаправляем на список новостей или статей в зависимости от типа поста
        return reverse_lazy('news_list' if self.object.post_type == 'news' else 'news_search')


