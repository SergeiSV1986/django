#from django_filters import FilterSet
#from newsportal.news.models import Post
#import django_filters


# Объявление фильтров Декларативный синтаксис
#class PostFiler(django_filters.FilterSet):
#    title__name = django_filters.CharFilter(lookup_expr='icontains')
#    author__name = django_filters.CharFilter(lookup_expr='icontains')
#    created_at__year = django_filters.NumberFilter(field_name='created_at__date', lookup_expr='year')
#    created_at__year__gt = django_filters.NumberFilter(field_name='created_at', lookup_expr='year__lt')
#    created_at__year__lt = django_filters.NumberFilter(field_name='created_at', lookup_expr='year__gt')

#    class Meta:
#        model = Post
#        fields = [
#            'title', 'author', 'created_at'

#       ]


from django_filters import FilterSet
from ..models import Post


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'title': ['icontains'],  # Поиск по названию
           'created_at': ['gte', 'lte'],  # Фильтрация по дате
       }

