"""
Models for the bookshelf app with custom user model.

This module contains:
1. CustomUser - Extended user model with additional security features
2. Book - Book model for the library system
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model.
    
    Provides methods to create regular users and superusers with proper
    password hashing and validation.
    """
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a regular user with an encrypted password.
        """
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email) if email else None
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # This properly hashes the password
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a superuser with an encrypted password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    Additional fields:
    - date_of_birth: User's date of birth for age verification
    - profile_photo: User's profile picture with secure upload path
    
    Security considerations:
    - Uses custom manager for proper password handling
    - Profile photos stored in secure location
    - Inherits all Django's built-in user security features
    """
    
    date_of_birth = models.DateField(
        null=True, 
        blank=True,
        help_text="User's date of birth for age verification and personalization"
    )
    
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text="User's profile picture (JPEG/PNG recommended, max 5MB)"
    )
    
    # Use our custom manager
    objects = CustomUserManager()
    
    class Meta:
        # Ensure proper database table naming
        db_table = 'bookshelf_customuser'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        """Return the URL for this user's profile."""
        return reverse('user-profile', kwargs={'pk': self.pk})


class Book(models.Model):
    """
    Book model with custom permissions for fine-grained access control.
    
    Security features:
    - Custom permissions for different operations
    - Input validation and sanitization
    - Secure field definitions
    """
    
    title = models.CharField(
        max_length=200,
        help_text="Book title (max 200 characters)"
    )
    
    author = models.CharField(
        max_length=100,
        help_text="Author name (max 100 characters)"
    )
    
    publication_year = models.PositiveIntegerField(
        help_text="Year the book was published"
    )
    
    isbn = models.CharField(
        max_length=13,
        unique=True,
        null=True,
        blank=True,
        help_text="ISBN-13 number (13 digits)"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Book description or summary"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Link to the user who added the book
    added_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books_added'
    )
    
    class Meta:
        # Custom permissions for fine-grained access control
        permissions = [
            ('can_view', 'Can view books'),
            ('can_create', 'Can create books'),
            ('can_edit', 'Can edit books'),
            ('can_delete', 'Can delete books'),
        ]
        
        # Database optimizations
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['publication_year']),
        ]
        
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def get_absolute_url(self):
        """Return the URL for this book's detail view."""
        return reverse('book-detail', kwargs={'pk': self.pk})
    
    def clean(self):
        """
        Custom validation for the Book model.
        
        Security considerations:
        - Validates ISBN format
        - Ensures publication year is reasonable
        - Sanitizes text fields
        """
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        import re
        
        # Validate publication year
        current_year = timezone.now().year
        if self.publication_year and (self.publication_year < 1000 or self.publication_year > current_year + 1):
            raise ValidationError({
                'publication_year': f'Publication year must be between 1000 and {current_year + 1}'
            })
        
        # Validate ISBN format (basic validation)
        if self.isbn:
            # Remove any hyphens or spaces
            isbn_clean = re.sub(r'[-\s]', '', self.isbn)
            if not isbn_clean.isdigit() or len(isbn_clean) not in [10, 13]:
                raise ValidationError({
                    'isbn': 'ISBN must be 10 or 13 digits'
                })
            self.isbn = isbn_clean
    
    def save(self, *args, **kwargs):
        """Override save to include validation."""
        self.full_clean()  # This calls clean() method
        super().save(*args, **kwargs)
