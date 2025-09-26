from rest_framework import serializers
from apps.article.models import Article, Category, Tag

# Teg nomini qabul qilib, uni bazadan qidiradigan yoki yangi yaratadigan maxsus maydon
class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            # Avval mavjud tegni nomi bo'yicha qidirib ko'ramiz
            tag, created = Tag.objects.get_or_create(**{self.slug_field: data})
            return tag
        except (TypeError, ValueError):
            self.fail('invalid')

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
            'id', 'title', 'slug', 'excerpt', 'featured_image', 
            'author', 'category', 'tags', 'status', 'published_at', 'view_count'
        ]
        read_only_fields = ['slug', 'published_at', 'view_count', 'author']


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    """Maqola yaratish va yangilash uchun serializer."""
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    tags = CreatableSlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name',
        required=False
    )

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
        ]
        read_only_fields = ['slug', 'published_at', 'view_count']

    # MUHIM O'ZGARISH: Maxsus 'update' metodini qaytaramiz
    def update(self, instance, validated_data):
        # Avval teglarni ma'lumotlardan ajratib olamiz
        tags_data = validated_data.pop('tags', None)

        # Qolgan barcha maydonlarni ota-klassning 'update' metodi orqali yangilaymiz
        # Bu 'setattr' orqali birma-bir yangilashdan ancha ishonchli
        instance = super().update(instance, validated_data)

        # Agar so'rovda teglar bo'lsa, ularni alohida yangilaymiz
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
            'id', 'title', 'slug', 'content', 'excerpt', 'featured_image', 
            'author', 'category', 'tags', 'status', 'published_at', 'view_count'
        ]
        read_only_fields = ['slug', 'published_at', 'view_count', 'author']

