"""
Views for the bookshelf app with comprehensive security measures.

This module provides:
1. Permission-protected views using @permission_required decorators
2. CSRF protection for all forms
3. Input validation and sanitization
4. Secure error handling
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.html import escape
from django.forms import ModelForm
from django import forms
from .models import Book, CustomUser
import logging

# Set up logging for security monitoring
logger = logging.getLogger(__name__)


class BookForm(ModelForm):
    """
    Secure form for Book model with validation.
    
    Security features:
    - Input validation
    - CSRF protection (handled by Django)
    - XSS prevention through proper field handling
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'isbn', 'description']
    
    def clean_title(self):
        """Validate and sanitize book title."""
        title = self.cleaned_data.get('title')
        if title:
            # Basic sanitization - Django handles most XSS prevention
            title = title.strip()
            if len(title) < 2:
                raise forms.ValidationError("Title must be at least 2 characters long.")
        return title
    
    def clean_isbn(self):
        """Validate ISBN format."""
        isbn = self.cleaned_data.get('isbn')
        if isbn:
            # Remove spaces and hyphens
            isbn = isbn.replace('-', '').replace(' ', '')
            if not isbn.isdigit() or len(isbn) not in [10, 13]:
                raise forms.ValidationError("ISBN must be 10 or 13 digits.")
        return isbn


# Function-based views with permission decorators

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
@require_http_methods(["GET"])
def book_list(request):
    """
    Display a list of books with search functionality.
    
    Security features:
    - Requires authentication and specific permission
    - Input sanitization for search queries
    - Pagination to prevent data exposure
    - SQL injection prevention through Django ORM
    """
    # Log the access attempt for security monitoring
    logger.info(f"User {request.user.username} accessed book list")
    
    # Get search query and sanitize it
    search_query = request.GET.get('search', '').strip()
    if search_query:
        # Escape the search query to prevent XSS
        search_query = escape(search_query)
        # Log search attempts for security monitoring
        logger.info(f"User {request.user.username} searched for: {search_query}")
    
    # Start with all books, using Django ORM to prevent SQL injection
    books = Book.objects.all().select_related('added_by')
    
    # Apply search filter if provided
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Implement pagination for security and performance
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page', 1)
    
    try:
        page_number = int(page_number)
    except (ValueError, TypeError):
        page_number = 1
    
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_books': paginator.count,
    }
    
    return render(request, 'bookshelf/book_list.html', context)


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def edit_book(request, book_id):
    """
    Edit a book with proper permission checking.
    
    Security features:
    - Requires authentication and edit permission
    - CSRF protection
    - Input validation through ModelForm
    - Secure error handling
    """
    # Get the book or return 404 (don't expose existence of non-existent IDs)
    book = get_object_or_404(Book, pk=book_id)
    
    # Log the edit attempt for security monitoring
    logger.info(f"User {request.user.username} attempting to edit book {book.id}")
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            try:
                # Save the book with audit trail
                updated_book = form.save()
                logger.info(f"User {request.user.username} successfully updated book {book.id}")
                messages.success(request, f'Book "{updated_book.title}" updated successfully.')
                return redirect('book-detail', pk=updated_book.pk)
            except Exception as e:
                # Log the error for security monitoring
                logger.error(f"Error updating book {book.id} by user {request.user.username}: {str(e)}")
                messages.error(request, 'An error occurred while updating the book. Please try again.')
        else:
            # Log validation errors
            logger.warning(f"Form validation failed for book {book.id} edit by user {request.user.username}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
    }
    
    return render(request, 'bookshelf/edit_book.html', context)


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def create_book(request):
    """
    Create a new book with proper permission checking.
    
    Security features:
    - Requires authentication and create permission
    - CSRF protection
    - Input validation
    - Audit trail
    """
    logger.info(f"User {request.user.username} accessing book creation form")
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                # Save the book and set the added_by field
                book = form.save(commit=False)
                book.added_by = request.user
                book.save()
                
                logger.info(f"User {request.user.username} created new book {book.id}")
                messages.success(request, f'Book "{book.title}" created successfully.')
                return redirect('book-detail', pk=book.pk)
            except Exception as e:
                logger.error(f"Error creating book by user {request.user.username}: {str(e)}")
                messages.error(request, 'An error occurred while creating the book. Please try again.')
        else:
            logger.warning(f"Form validation failed for book creation by user {request.user.username}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'bookshelf/create_book.html', context)


# Class-based views with permission mixins

class SecureBookListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Class-based view for book listing with enhanced security.
    
    Security features:
    - Login required
    - Permission checking
    - Pagination
    - Query optimization
    """
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view'
    paginate_by = 10
    
    def get_queryset(self):
        """Override to add search and optimization."""
        queryset = super().get_queryset().select_related('added_by')
        search_query = self.request.GET.get('search')
        
        if search_query:
            search_query = escape(search_query.strip())
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query)
            )
        
        return queryset.order_by('title')
    
    def get_context_data(self, **kwargs):
        """Add additional context."""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class SecureBookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Secure book detail view.
    
    Security features:
    - Authentication required
    - Permission checking
    - Safe error handling
    """
    model = Book
    template_name = 'bookshelf/book_detail.html'
    context_object_name = 'book'
    permission_required = 'bookshelf.can_view'
    
    def get_object(self, queryset=None):
        """Override to add logging."""
        obj = super().get_object(queryset)
        logger.info(f"User {self.request.user.username} viewed book {obj.id}")
        return obj


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
@csrf_protect
@require_http_methods(["POST"])
def delete_book(request, book_id):
    """
    Delete a book with proper permission checking.
    
    Security features:
    - POST-only method to prevent CSRF
    - Permission checking
    - Audit logging
    - Safe error handling
    """
    book = get_object_or_404(Book, pk=book_id)
    
    try:
        book_title = book.title
        book.delete()
        logger.info(f"User {request.user.username} deleted book {book_id} ({book_title})")
        messages.success(request, f'Book "{book_title}" deleted successfully.')
    except Exception as e:
        logger.error(f"Error deleting book {book_id} by user {request.user.username}: {str(e)}")
        messages.error(request, 'An error occurred while deleting the book.')
    
    return redirect('book-list')


# Utility views

@login_required
def home(request):
    """
    Secure home page view.
    
    Shows dashboard with user-specific information.
    """
    # Check if user has any book permissions
    has_view_permission = request.user.has_perm('bookshelf.can_view')
    has_create_permission = request.user.has_perm('bookshelf.can_create')
    has_edit_permission = request.user.has_perm('bookshelf.can_edit')
    has_delete_permission = request.user.has_perm('bookshelf.can_delete')
    
    context = {
        'user': request.user,
        'has_view_permission': has_view_permission,
        'has_create_permission': has_create_permission,
        'has_edit_permission': has_edit_permission,
        'has_delete_permission': has_delete_permission,
    }
    
    # If user can view books, show recent books
    if has_view_permission:
        context['recent_books'] = Book.objects.all()[:5]
        context['total_books'] = Book.objects.count()
    
    return render(request, 'bookshelf/home.html', context)


# AJAX views for enhanced security

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
@require_http_methods(["GET"])
def book_search_api(request):
    """
    AJAX endpoint for book search.
    
    Security features:
    - JSON response only
    - Permission checking
    - Input sanitization
    - Rate limiting ready
    """
    search_query = request.GET.get('q', '').strip()
    
    if not search_query or len(search_query) < 2:
        return JsonResponse({'error': 'Search query must be at least 2 characters'}, status=400)
    
    # Sanitize the search query
    search_query = escape(search_query)
    
    # Limit results for performance and security
    books = Book.objects.filter(
        Q(title__icontains=search_query) |
        Q(author__icontains=search_query)
    )[:10]  # Limit to 10 results
    
    results = [
        {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'year': book.publication_year,
        }
        for book in books
    ]
    
    return JsonResponse({'results': results})


# Error handlers

def permission_denied_view(request, exception):
    """
    Custom permission denied handler.
    
    Security: Provides user-friendly error messages without exposing system details.
    """
    logger.warning(f"Permission denied for user {request.user.username} on {request.path}")
    return render(request, 'bookshelf/403.html', status=403)


def handler404(request, exception):
    """Custom 404 handler."""
    return render(request, 'bookshelf/404.html', status=404)


def handler500(request):
    """Custom 500 handler."""
    logger.error(f"Server error on {request.path} for user {request.user.username}")
    return render(request, 'bookshelf/500.html', status=500)
