import django_filters
from apps.article.models import Article

class ArticleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="iexact")
    tag = django_filters.CharFilter(field_name="tags__slug", lookup_expr="iexact")
    author = django_filters.CharFilter(field_name="author__username", lookup_expr="iexact")
    date_from = django_filters.DateFilter(field_name="published_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="published_at", lookup_expr="lte")

    class Meta:
        model = Article
        fields = ["category", "tag", "author", "date_from", "date_to"]
