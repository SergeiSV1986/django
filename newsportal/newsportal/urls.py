"""
URL configuration for newsportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from news.views import NewsListView, NewsSearchView, news_detail

urlpatterns = [
    path('admin/', admin.site.urls),
  #Делаем так, чтобы все адреса из нашего приложения
  # подключались к главному приложению
    path('', include('news.urls')),
   # path('news/', NewsListView.as_view(), name='news_list'),  # Список новостей
   # path('news/<int:news_id>/', NewsDetailView.as_view(), name='news_detail'),  # Детали новости
    #path('search/', NewsSearchView.as_view(), name='news_search'),  # Поиск новостей
]
