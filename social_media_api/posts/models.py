from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Post(models.Model):
    """
    Model representing a user's post in the social media platform.
    """
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts',
        help_text="The user who created this post"
    )
    content = models.TextField(help_text="The text content of the post")
    image = models.ImageField(
        upload_to='posts/images/', 
        blank=True, 
        null=True,
        help_text="Optional image for the post"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'posts_post'

    def __str__(self):
        return f"{self.author.username} - {self.content[:50]}..."

    @property
    def likes_count(self):
        """Return the number of likes for this post"""
        return self.likes.count()

    @property
    def comments_count(self):
        """Return the number of comments for this post"""
        return self.comments.count()


class Comment(models.Model):
    """
    Model representing a comment on a post.
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text="The post this comment belongs to"
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text="The user who wrote this comment"
    )
    text = models.TextField(help_text="The comment text")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'posts_comment'

    def __str__(self):
        return f"{self.author.username} on {self.post.id}: {self.text[:30]}..."


class Like(models.Model):
    """
    Model representing a like on a post.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='likes',
        help_text="The user who liked the post"
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='likes',
        help_text="The post that was liked"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        db_table = 'posts_like'

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"
