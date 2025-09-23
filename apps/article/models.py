from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()
# Kategoriya modeli
class Category(models.Model):
    """
    Maqolalar uchun kategoriya modeli.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name="Ota kategoriya"
    )

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

    def __str__(self):
        return self.name

# Teg modeli
class Tag(models.Model):
    """
    Maqolalar uchun teg modeli.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="Teg nomi")
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    class Meta:
        verbose_name = "Teg"
        verbose_name_plural = "Teglar"
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Yangiliklar va maqolalar uchun asosiy model.
    """
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Qoralama'
        PUBLISHED = 'PUBLISHED', 'Nashr qilingan'
        ARCHIVED = 'ARCHIVED', 'Arxivlangan'

    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(verbose_name="Asosiy matn")
    excerpt = models.TextField(blank=True, verbose_name="Qisqa tavsif (anons)")
    featured_image = models.ImageField(upload_to='articles/%Y/%m/%d/', verbose_name="Asosiy rasm")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    # Bog'liqliklar (Relationships)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # Muallif o'chirilsa, maqolalari o'chib ketmaydi
        null=True,
        related_name='articles',
        verbose_name="Muallif"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, # Kategoriya o'chirilsa, maqolalari o'chmaydi
        null=True,
        related_name='articles',
        verbose_name="Kategoriya"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles',
        verbose_name="Teglar"
    )
    
    # Holat va statistika
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    view_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    
    # Vaqtlar
    published_at = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name="Nashr qilingan sana")

    class Meta:
        ordering = ['-published_at'] # Eng yangi maqolalar tepad turadi
        verbose_name = "Maqola"
        verbose_name_plural = "Maqolalar"

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    """
    Maqolalarga yozilgan izohlar.
    """
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE, # Maqola o'chirilsa, uning izohlari ham o'chadi
        related_name='comments',
        verbose_name="Maqola"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Muallif"
    )
    content = models.TextField(verbose_name="Izoh matni")
    
    # Ichma-ich izohlar uchun
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    is_active = models.BooleanField(default=True, help_text="Admin tomonidan tasdiqlangan izohlar saytda ko'rinadi.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] # Eng eski izohlar birinchi ko'rinadi
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"

    def __str__(self):
        return f"'{self.author}'ning '{self.article.title}' maqolasiga izohi"
