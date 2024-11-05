from django_filters import FilterSet
from .models import Post
import django_filters


# Объявление фильтров Декларативный синтаксис
class PostFiler(django_filters.FilterSet):
    title__name = django_filters.CharFilter(lookup_expr='icontains')
    author__name = django_filters.CharFilter(lookup_expr='icontains')
    created_at__year = django_filters.NumberFilter(field_name='created_at__date', lookup_expr='year')
    created_at__year__gt = django_filters.NumberFilter(field_name='created_at', lookup_expr='year__lt')
    created_at__year__lt = django_filters.NumberFilter(field_name='created_at', lookup_expr='year__gt')

    class Meta:
        model = Post
        fields = [
            'title', 'author', 'created_at'

        ]