import django_filters
from apps.article.models import Article

class ArticleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    tags = django_filters.CharFilter(field_name='tags__slug')
    author = django_filters.CharFilter(field_name='author__username')
    status = django_filters.ChoiceFilter(choices=Article.Status.choices)
    published_after = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='gte')
    published_before = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='lte')

    class Meta:
        model = Article
        fields = ['category', 'tags', 'author', 'status', 'published_after', 'published_before']