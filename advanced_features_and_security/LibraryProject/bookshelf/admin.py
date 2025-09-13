from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser model.
    """
    # Add the custom fields to the admin interface
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )
    
    # Add custom fields to the add user form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )
    
    # Display these fields in the user list
    list_display = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff']
    list_filter = UserAdmin.list_filter + ('date_of_birth',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for Book model with enhanced features.
    """
    list_display = ['title', 'author', 'publication_year', 'isbn', 'added_by', 'created_at']
    list_filter = ['publication_year', 'created_at', 'updated_at', 'added_by']
    search_fields = ['title', 'author', 'isbn', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year', 'isbn', 'description')
        }),
        ('Metadata', {
            'fields': ('added_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Set the user who adds the book automatically
    def save_model(self, request, obj, form, change):
        if not change:  # Only set on creation
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
