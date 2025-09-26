# api_endpoints/for_readers/views.py
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics, permissions, filters
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.article.models import Article, Tag, Category, Comment

from .serializers import (
    CategorySerializer,
    ArticleListSerializer,
    ArticleDetailSerializer,
    TagSerializer,
    CommentSerializer,
)
from .filters import ArticleFilter


class CategoryListAPIView(generics.ListAPIView):
    """
    Barcha kategoriyalar ro‘yxati
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryArticleListAPIView(generics.ListAPIView):
    """
    Bitta kategoriya uchun maqolalar ro‘yxati
    """
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return (
            Article.objects.filter(
                category__slug=slug,
                status=Article.Status.PUBLISHED
            )
            .select_related("author", "category")
            .prefetch_related("tags")
            .order_by("-published_at")
        )

class ArticleListAPIView(generics.ListAPIView):
    """
    GET /api/articles/
    Filtirlar: ?category=<slug>&tag=<slug>&author=<username>&date_from=&date_to=
    Ordering: ?ordering=-published_at or ?ordering=view_count
    Pagination: LimitOffsetPagination (settings orqali)
    """
    serializer_class = ArticleListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # search handled by your MultiSymbolSearchFilter globally
    filterset_class = ArticleFilter
    ordering_fields = ["published_at", "view_count", "comment_count"]
    ordering = ["-published_at"]

    def get_queryset(self):
        # faqat nashr qilingan maqolalar
        qs = (
            Article.objects.filter(status=Article.Status.PUBLISHED)
            .select_related("author", "category")
            .prefetch_related("tags")
            .annotate(
                comment_count=Count("comments", filter=Q(comments__is_active=True))
            )
            .distinct()
        )
        return qs


class ArticleDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/articles/<slug>/
    Maqola detail qaytaradi va view_count ni atomik ravishda oshiradi.
    """
    serializer_class = ArticleDetailSerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]

    # (ixtiyoriy) bu endpointni cache qilish mumkin — kerak bo'lsa uncomment qiling:
    # @method_decorator(cache_page(60 * 5), name="dispatch")
    def get_queryset(self):
        return (
            Article.objects.filter(status=Article.Status.PUBLISHED)
            .select_related("author", "category")
            .prefetch_related("tags", "comments__author")
            .annotate(
                comment_count=Count("comments", filter=Q(comments__is_active=True))
            )
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # atomic increment
        Article.objects.filter(pk=instance.pk).update(view_count=F("view_count") + 1)
        # yangilangan view_count ni olish
        instance.refresh_from_db(fields=["view_count"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TagListAPIView(generics.ListAPIView):
    """
    GET /api/tags/  -> barcha teglar va har bir tag uchun annotatsiya (nashr qilingan maqolalar soni).
    """
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Tag.objects.all().annotate(
        article_count=Count("articles", filter=Q(articles__status=Article.Status.PUBLISHED))
    )


class ArticlesByTagAPIView(generics.ListAPIView):
    """
    GET /api/tags/<slug>/articles/  -> berilgan tegga tegishli nashr qilingan maqolalar
    """
    serializer_class = ArticleListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ["-published_at"]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return (
            Article.objects.filter(status=Article.Status.PUBLISHED, tags__slug__iexact=slug)
            .select_related("author", "category")
            .prefetch_related("tags")
            .annotate(
                comment_count=Count("comments", filter=Q(comments__is_active=True))
            )
            .distinct()
        )


class ArticlesByCategoryAPIView(generics.ListAPIView):
    """
    GET /api/categories/<slug>/articles/  -> berilgan kategoriya bo'yicha nashr qilingan maqolalar
    """
    serializer_class = ArticleListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ["-published_at"]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return (
            Article.objects.filter(status=Article.Status.PUBLISHED, category__slug__iexact=slug)
            .select_related("author", "category")
            .prefetch_related("tags")
            .annotate(
                comment_count=Count("comments", filter=Q(comments__is_active=True))
            )
            .distinct()
        )


class ArticleCommentsAPIView(generics.ListCreateAPIView):
    """
    GET /api/articles/<slug>/comments/   -> top-level (parent=None) active comments
    POST /api/articles/<slug>/comments/  -> create comment (auth required)
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return (
            Comment.objects.filter(article__slug=slug, is_active=True, parent=None)
            .select_related("author", "article")
            .prefetch_related("replies", "replies__author")
            .order_by("created_at")
        )

    def perform_create(self, serializer):
        slug = self.kwargs.get("slug")
        article = get_object_or_404(Article, slug=slug, status=Article.Status.PUBLISHED)
        serializer.save(author=self.request.user, article=article)

__all__ = [
    "CategoryListAPIView",
    "CategoryArticleListAPIView",
    "ArticleListAPIView",
    "ArticleDetailAPIView",
    "TagListAPIView",
    "ArticlesByTagAPIView",
    "ArticlesByCategoryAPIView",
    "ArticleCommentsAPIView",
]