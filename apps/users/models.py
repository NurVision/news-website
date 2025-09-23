from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        EDITOR = 'EDITOR', 'Muharrir'
        READER = 'READER', 'O\'quvchi'
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.READER)
    avatar = models.ImageField(upload_to='staticfiles/avatars/', null=True, blank=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']