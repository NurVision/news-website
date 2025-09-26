from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied # <-- Yaxshiroq xatolik uchun
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from apps.article.models import Article
from .serializers import (
    ArticleListSerializer,
    ArticleCreateUpdateSerializer,
    ArticleDetailSerializer
)
from .permissions import IsEditorOrAdmin
from drf_yasg.utils import swagger_auto_schema

# Maqolalar ro'yxatini ko'rish va yangi maqola yaratish uchun
class ArticleListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEditorOrAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        articles = (
            Article.objects.filter(author=request.user)
            .select_related("author", "category")   
            .prefetch_related("tags")               
            .order_by("-published_at")
        )
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ArticleCreateUpdateSerializer)
    def post(self, request):
        serializer = ArticleCreateUpdateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            # Serializer'ning o'zi author'ni belgilaydi (CurrentUserDefault orqali)
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Maqolani ko'rish, yangilash va o'chirish uchun
class ArticleRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEditorOrAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        article = get_object_or_404(Article, pk=pk)
        # Ruxsatni tekshirishning standart usuli
        if article.author != self.request.user:
            raise PermissionDenied("Sizda bu maqolani tahrirlashga ruxsat yo'q.")
        return article

    def get(self, request, pk):
        article = (
            Article.objects.select_related("author", "category")
            .prefetch_related("tags")
            .get(pk=pk)
        )
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ArticleCreateUpdateSerializer)
    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleCreateUpdateSerializer(article, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ArticleCreateUpdateSerializer)
    def patch(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleCreateUpdateSerializer(article, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

__all__ = ['ArticleListCreateAPIView', 'ArticleRetrieveUpdateDestroyAPIView']
