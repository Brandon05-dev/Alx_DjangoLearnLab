from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the custom User model.
    """
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'profile_picture', 'followers')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'profile_picture')
        }),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'followers_count', 'following_count', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    def followers_count(self, obj):
        return obj.followers_count
    followers_count.short_description = 'Followers'
    
    def following_count(self, obj):
        return obj.following_count
    following_count.short_description = 'Following'
