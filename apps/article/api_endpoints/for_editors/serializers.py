from rest_framework import serializers
from apps.article.models import Article, Category, Tag

class TagSerializer(serializers.ModelSerializer):
    """Teglar uchun serializer."""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']

class CategorySerializer(serializers.ModelSerializer):
    """Kategoriyalar uchun serializer."""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']

class ArticleListSerializer(serializers.ModelSerializer):
    """Maqolalar ro'yxati uchun serializer."""
    author = serializers.CharField(source='author.username', read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 
            'title', 
            'slug', 
            'excerpt', 
            'featured_image', 
            'author', 
            'category', 
            'tags', 
            'status', 
            'published_at',
            'view_count'
        ]
        read_only_fields = ['slug', 'published_at', 'view_count', 'author']


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    """Maqola yaratish va yangilash uchun serializer."""
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'excerpt',
            'featured_image',
            'author',
            'category',
            'tags',
            'status'
        ]
        read_only_fields = ['slug', 'published_at', 'view_count']

    def create(self, validated_data):
        """Yangi maqola yaratish metodi."""
        tags_data = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)
        article.tags.set(tags_data)
        return article
    
    def update(self, instance, validated_data):
        """Maqolani yangilash metodi."""
        tags_data = validated_data.pop('tags', None)
        
        # Maydonlarni yangilash
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Maqolani saqlash
        instance.save()

        # Teglarni yangilash (agar mavjud bo'lsa)
        if tags_data is not None:
            instance.tags.set(tags_data)
        
        return instance
    
class ArticleDetailSerializer(serializers.ModelSerializer):
    """Maqola tafsilotlari uchun serializer."""
    author = serializers.CharField(source='author.username', read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 
            'title', 
            'slug', 
            'content', 
            'excerpt', 
            'featured_image', 
            'author', 
            'category', 
            'tags', 
            'status', 
            'published_at',
            'view_count'
        ]
        read_only_fields = ['slug', 'published_at', 'view_count', 'author']
