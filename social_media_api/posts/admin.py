from django.contrib import admin
from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post model.
    """
    list_display = ['id', 'author', 'content_preview', 'likes_count', 'comments_count', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'likes_count', 'comments_count']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Comment model.
    """
    list_display = ['id', 'author', 'post_id', 'text_preview', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['text', 'author__username', 'post__content']
    readonly_fields = ['created_at', 'updated_at']
    
    def text_preview(self, obj):
        return obj.text[:30] + '...' if len(obj.text) > 30 else obj.text
    text_preview.short_description = 'Text Preview'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Like model.
    """
    list_display = ['id', 'user', 'post_id', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__content']
    readonly_fields = ['created_at']
