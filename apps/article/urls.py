from django.urls import path

from apps.article.api_endpoints.for_editors.views import ArticleRetrieveUpdateDestroyAPIView
from .api_endpoints import (
    CategoryListAPIView,
    CategoryArticleListAPIView,
    ArticleListAPIView,
    ArticleDetailAPIView,
    TagListAPIView,
    ArticlesByTagAPIView,
    ArticlesByCategoryAPIView,
    ArticleCommentsAPIView,

    ArticleListCreateAPIView,
    ArticleRetrieveUpdateDestroyAPIView    
)

app_name = "article"

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path("categories/<slug>/articles/", CategoryArticleListAPIView.as_view(), name="category-article-list   "),
    path("articles/", ArticleListAPIView.as_view(), name="article-list"),
    path("articles/<slug>/", ArticleDetailAPIView.as_view(), name="article-detail"),            
    path("tags/", TagListAPIView.as_view(), name="tag-list"),
    path("tags/<slug>/articles/", ArticlesByTagAPIView.as_view(), name="articles-by-tag"),
    path("categories/<slug>/articles/", ArticlesByCategoryAPIView.as_view(), name="articles-by-category"),
    path("articles/<slug>/comments/", ArticleCommentsAPIView.as_view(), name="article-comments"),

    # Editor endpoints
    path("editor/articles/", ArticleListCreateAPIView.as_view(), name="editor-article-list-create"),
    path("editor/articles/<int:pk>/", ArticleRetrieveUpdateDestroyAPIView.as_view(), name="editor-article-detail"),
]