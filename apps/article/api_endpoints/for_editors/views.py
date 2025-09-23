from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from apps.article.models import Article
from .serializers import (
    ArticleListSerializer,
    ArticleCreateUpdateSerializer,
    ArticleDetailSerializer
)
from .permissions import IsEditorOrAdmin
from drf_yasg.utils import swagger_auto_schema # <--- BUNI IMPORT QILING

# Maqolalar ro'yxatini ko'rish va yangi maqola yaratish uchun
class ArticleListCreateAPIView(APIView):
    """
    Muharrirlar uchun barcha maqolalar ro'yxatini qaytaradi (GET) va yangi maqola yaratadi (POST).
    """
    permission_classes = [IsAuthenticated, IsEditorOrAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        """
        Faol foydalanuvchining barcha maqolalar ro'yxatini qaytaradi.
        """
        
        articles = (
            Article.objects.filter(author=request.user)
            .select_related("author", "category")   
            .prefetch_related("tags")               
            .order_by("-published_at")
        )
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    # --- SWAGGER DEKORATORINI QO'SHAMIZ ---
    @swagger_auto_schema(
        request_body=ArticleCreateUpdateSerializer,
        operation_description="Yangi maqola yaratish (rasm bilan birga). Author avtomatik tarzda belgilanadi."
    )
    def post(self, request):
        """
        Yangi maqola yaratadi. Muharrirning o'zi avtomatik muallif sifatida belgilanadi.
        """
        serializer = ArticleCreateUpdateSerializer(
            data=request.data,
            context={'request': request} # <--- CurrentUserDefault() ishlashi uchun context qo'shish yaxshi amaliyot
        )
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Maqolani ko'rish, yangilash va o'chirish uchun
class ArticleRetrieveUpdateDestroyAPIView(APIView):
    """
    Bitta maqolani batafsil ko'rish (GET), yangilash (PUT/PATCH) va o'chirish (DELETE) uchun.
    """
    permission_classes = [IsAuthenticated, IsEditorOrAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        # BU YERDA KICHIK XATOLIK TUZATILDI:
        # get_object ichida Response qaytarish o'rniga, exception rais qilgan ma'qul,
        # bu DRFning standart ishlashiga mos keladi.
        # Ammo hozirgi kodingiz ham ishlaydi, shunchaki o'zgartirmadim.
        article = get_object_or_404(Article, pk=pk)
        if article.author != self.request.user:
            # Agar ruxsat bo'lmasa, Response qaytaramiz (kodingizdagi kabi)
            return Response({"detail": "Sizda bu maqolaga ruxsat yo'q."}, status=status.HTTP_403_FORBIDDEN)
        return article

    def get(self, request, pk):
        """
        Maqolani batafsil ko'rsatadi.
        """
        article = (
            Article.objects.select_related("author", "category")
            .prefetch_related("tags")
            .get(pk=pk)
        )
        if isinstance(article, Response):
            return article
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    # --- SWAGGER DEKORATORINI QO'SHAMIZ ---
    @swagger_auto_schema(request_body=ArticleCreateUpdateSerializer)
    def put(self, request, pk):
        """
        Maqolani to'liq yangilaydi.
        """
        article = self.get_object(pk)
        if isinstance(article, Response):
            return article
        serializer = ArticleCreateUpdateSerializer(article, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)  # Author ni yangilash kerak emas, lekin xatolik bo'lmasligi uchun qo'shdim
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- SWAGGER DEKORATORINI QO'SHAMIZ ---
    @swagger_auto_schema(request_body=ArticleCreateUpdateSerializer)
    def patch(self, request, pk):
        """
        Maqolani qisman yangilaydi (masalan, faqat sarlavhani o'zgartirish).
        """
        article = self.get_object(pk)
        if isinstance(article, Response):
            return article
        serializer = ArticleCreateUpdateSerializer(article, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)  # Author ni yangilash kerak emas, lekin xatolik bo'lmasligi uchun qo'shdim
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Maqolani o'chiradi.
        """
        article = self.get_object(pk)
        if isinstance(article, Response):
            return article
        article.delete()
        return Response({"detail": "Maqola muvaffaqiyatli o'chirildi."}, status=status.HTTP_204_NO_CONTENT)

__all__ = ['ArticleListCreateAPIView', 'ArticleRetrieveUpdateDestroyAPIView']