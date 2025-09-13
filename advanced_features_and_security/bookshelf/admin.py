"""
Admin configuration for the bookshelf app with enhanced security.

This module provides:
1. CustomUserAdmin - Enhanced admin interface for CustomUser
2. BookAdmin - Admin interface for Book model with permissions
3. Security-focused admin configurations
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from .models import CustomUser, Book


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form for admin interface.
    
    Security considerations:
    - Inherits Django's built-in password validation
    - Includes additional fields for our CustomUser model
    """
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'date_of_birth', 'profile_photo')


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form for admin interface.
    
    Security considerations:
    - Maintains Django's password handling security
    - Provides safe editing of additional fields
    """
    
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Enhanced admin interface for CustomUser model.
    
    Security features:
    - Displays additional fields safely
    - Maintains Django's built-in user security
    - Provides secure image display
    - Includes audit information
    """
    
    # Forms for adding and changing users
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    # Display fields in the user list
    list_display = [
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'date_of_birth',
        'is_staff',
        'is_active',
        'date_joined',
        'profile_photo_display'
    ]
    
    # Fields that can be searched
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    # Filters in the admin sidebar
    list_filter = [
        'is_staff', 
        'is_superuser', 
        'is_active', 
        'date_joined',
        'date_of_birth'
    ]
    
    # Fields to display when editing a user
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
            'classes': ('collapse',),  # Make this section collapsible
        }),
    )
    
    # Fields to display when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('email', 'date_of_birth', 'profile_photo'),
            'classes': ('collapse',),
        }),
    )
    
    def profile_photo_display(self, obj):
        """
        Safely display profile photo in admin list.
        
        Security considerations:
        - Uses Django's format_html for safe HTML rendering
        - Provides fallback for missing images
        - Limits image size for performance
        """
        if obj.profile_photo:
            return format_html(
                '<img src="{}" style="width: 30px; height: 30px; border-radius: 50%; object-fit: cover;" />',
                obj.profile_photo.url
            )
        return format_html('<span style="color: #999;">No photo</span>')
    
    profile_photo_display.short_description = 'Photo'
    
    def get_readonly_fields(self, request, obj=None):
        """
        Make certain fields read-only based on user permissions.
        
        Security: Prevents unauthorized modification of critical fields.
        """
        readonly_fields = super().get_readonly_fields(request, obj)
        
        # Make date_joined read-only for non-superusers
        if not request.user.is_superuser:
            readonly_fields = list(readonly_fields) + ['date_joined', 'last_login']
        
        return readonly_fields


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for Book model with security considerations.
    
    Security features:
    - Displays audit fields
    - Implements proper permissions
    - Provides secure data handling
    """
    
    # Display fields in the book list
    list_display = [
        'title',
        'author', 
        'publication_year',
        'isbn',
        'added_by',
        'created_at',
        'book_link'
    ]
    
    # Fields that can be searched
    search_fields = ['title', 'author', 'isbn', 'description']
    
    # Filters in the admin sidebar
    list_filter = [
        'publication_year',
        'created_at',
        'updated_at',
        'added_by'
    ]
    
    # Fields to display when editing a book
    fieldsets = [
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year', 'isbn', 'description')
        }),
        ('Metadata', {
            'fields': ('added_by',),
            'classes': ('collapse',),
        }),
        ('Audit Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    ]
    
    # Read-only fields for audit trail
    readonly_fields = ['created_at', 'updated_at']
    
    # Order by title by default
    ordering = ['title']
    
    # Number of items per page
    list_per_page = 25
    
    def book_link(self, obj):
        """
        Provide a safe link to the book's detail page.
        
        Security: Uses Django's URL reversing for safe link generation.
        """
        try:
            url = reverse('book-detail', kwargs={'pk': obj.pk})
            return format_html('<a href="{}" target="_blank">View</a>', url)
        except:
            return 'N/A'
    
    book_link.short_description = 'View Book'
    
    def save_model(self, request, obj, form, change):
        """
        Override save to automatically set the added_by field.
        
        Security: Ensures proper audit trail by tracking who added/modified books.
        """
        if not change:  # If this is a new object
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """
        Optimize queries for better performance.
        
        Security: Prevents N+1 query vulnerabilities.
        """
        return super().get_queryset(request).select_related('added_by')
    
    def has_delete_permission(self, request, obj=None):
        """
        Control delete permissions based on custom permissions.
        
        Security: Implements fine-grained permission control.
        """
        return request.user.has_perm('bookshelf.can_delete')
    
    def has_change_permission(self, request, obj=None):
        """
        Control change permissions based on custom permissions.
        
        Security: Implements fine-grained permission control.
        """
        return request.user.has_perm('bookshelf.can_edit')
    
    def has_add_permission(self, request):
        """
        Control add permissions based on custom permissions.
        
        Security: Implements fine-grained permission control.
        """
        return request.user.has_perm('bookshelf.can_create')


# Customize admin site headers for better branding and security awareness
admin.site.site_header = "Library Management System - Secure Admin"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Secure Administration Panel"

# Register Permission model for easier group management
admin.site.register(Permission)


class PermissionAdmin(admin.ModelAdmin):
    """Admin interface for managing permissions."""
    list_display = ['name', 'content_type', 'codename']
    list_filter = ['content_type']
    search_fields = ['name', 'codename']


# Unregister and re-register with custom admin
admin.site.unregister(Permission)
admin.site.register(Permission, PermissionAdmin)
