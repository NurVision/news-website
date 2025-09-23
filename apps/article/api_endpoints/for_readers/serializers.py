from rest_framework import serializers
from apps.article.models import Category, Tag, Article, Comment
from django.contrib.auth import get_user_model
import math

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Faqat maqola ko‘rish uchun kategoriyalar"""

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]


class TagSerializer(serializers.ModelSerializer):
    """Teglar uchun serializer"""

    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class CommentSerializer(serializers.ModelSerializer):
    """Izohlar va ichki izohlar (replies)"""
    author = serializers.CharField(source="author.username", read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "content",
            "created_at",
            "replies",
        ]

    def get_replies(self, obj):
        """Ichma-ich izohlarni recursive ko‘rsatish"""
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class ArticleListSerializer(serializers.ModelSerializer):
    """Maqolalar ro‘yxati uchun serializer"""
    author = serializers.CharField(source="author.username", read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    # Yangi maydonlar
    tag_list = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
        source="tags"
    )
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "featured_image",
            "author",
            "category",
            "tags",
            "tag_list",
            "published_at",
            "view_count",
            "reading_time",
        ]

    def get_reading_time(self, obj):
        """Matn uzunligiga qarab taxminiy o‘qish vaqti (daqiqa)"""
        words = obj.content.split()
        minutes = math.ceil(len(words) / 200)  # 200 ta so‘z = 1 daqiqa
        return f"{minutes} daqiqa"


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Bitta maqola detali uchun serializer"""
    author = serializers.CharField(source="author.username", read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    # Yangi maydonlar
    tag_list = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
        source="tags"
    )
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "excerpt",
            "featured_image",
            "author",
            "category",
            "tags",
            "tag_list",
            "status",
            "view_count",
            "published_at",
            "reading_time",
            "comments",
        ]

    def get_reading_time(self, obj):
        words = obj.content.split()
        minutes = math.ceil(len(words) / 200)
        return f"{minutes} daqiqa"
