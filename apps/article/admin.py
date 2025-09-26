from django.contrib import admin
from apps.article.models import Article, Category, Tag, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'published_at')
    search_fields = ('title', 'content')
    list_filter = ('status', 'published_at', 'category', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-published_at',)
    list_select_related = ('author', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    list_select_related = ('parent',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_at')
    search_fields = ('article__title', 'author__username', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
