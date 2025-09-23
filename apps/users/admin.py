from django.contrib import admin

from apps.users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('role',)
    ordering = ('-date_joined',)
    