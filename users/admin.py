"""
Admin interface for User model.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for User model.
    """
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'date_created']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_created']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_created']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('image', 'date_created', 'date_updated')}),
    )
    
    readonly_fields = ['date_created', 'date_updated'] 