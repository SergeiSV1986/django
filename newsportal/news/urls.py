from django.urls import path
# Импортируем созданное нами представление
from .views import NewsListView, news_detail, NewsSearchView, NewsCreate, ArticleCreate, ArticleUpdate, ArticleDelete
from django_filters.views import FilterView

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем авторам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   # path('', PostList.as_view()),
   path('news/', NewsListView.as_view(), name='news_list'),
   path('news/<int:news_id>/', news_detail, name='news_detail'),
   path('news/search/', NewsSearchView.as_view(), name='news_search'),
   # Маршрут для создания новостей
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   # Маршрут для редактирования новостей по их первичному ключу (pk)
   path('news/<int:pk>/edit/', ArticleUpdate.as_view(), name='news_edit'),
   # Маршрут для удаления новостей по их первичному ключу (pk)
   path('news/<int:pk>/delete/', ArticleDelete.as_view(), name='news_delete'),
   # Маршрут для создания статей
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   # Маршрут для редактирования статей по их первичному ключу (pk)
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
   # Маршрут для удаления статей по их первичному ключу (pk)
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]