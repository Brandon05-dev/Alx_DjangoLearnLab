from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Book, CustomUser


class BookListView(LoginRequiredMixin, ListView):
    """
    Display a list of books with security checks.
    """
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    paginate_by = 10
    
    def get_queryset(self):
        """Filter books based on user permissions."""
        if self.request.user.has_perm('bookshelf.can_view'):
            return Book.objects.all()
        else:
            # Users can only see books they added
            return Book.objects.filter(added_by=self.request.user)


class BookDetailView(LoginRequiredMixin, DetailView):
    """
    Display book details with permission checks.
    """
    model = Book
    template_name = 'bookshelf/book_detail.html'
    context_object_name = 'book'
    
    def get_queryset(self):
        """Ensure users can only view books they have permission to see."""
        if self.request.user.has_perm('bookshelf.can_view'):
            return Book.objects.all()
        else:
            return Book.objects.filter(added_by=self.request.user)


class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Create new books with proper security checks.
    """
    model = Book
    fields = ['title', 'author', 'publication_year', 'isbn', 'description']
    template_name = 'bookshelf/book_form.html'
    permission_required = 'bookshelf.can_create'
    success_url = reverse_lazy('book-list')
    
    def form_valid(self, form):
        """Set the user who created the book."""
        form.instance.added_by = self.request.user
        messages.success(self.request, 'Book added successfully!')
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Update books with permission and ownership checks.
    """
    model = Book
    fields = ['title', 'author', 'publication_year', 'isbn', 'description']
    template_name = 'bookshelf/book_form.html'
    permission_required = 'bookshelf.can_edit'
    
    def get_queryset(self):
        """Users can only edit books they added or if they have global edit permission."""
        if self.request.user.has_perm('bookshelf.can_edit'):
            return Book.objects.all()
        else:
            return Book.objects.filter(added_by=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete books with proper permission checks.
    """
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    permission_required = 'bookshelf.can_delete'
    success_url = reverse_lazy('book-list')
    
    def get_queryset(self):
        """Users can only delete books they added or if they have global delete permission."""
        if self.request.user.has_perm('bookshelf.can_delete'):
            return Book.objects.all()
        else:
            return Book.objects.filter(added_by=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_search(request):
    """
    Search for books with security checks.
    """
    query = request.GET.get('q', '')
    books = []
    
    if query:
        if request.user.has_perm('bookshelf.can_view'):
            books = Book.objects.filter(
                title__icontains=query
            ) | Book.objects.filter(
                author__icontains=query
            )
        else:
            books = Book.objects.filter(
                added_by=request.user,
                title__icontains=query
            ) | Book.objects.filter(
                added_by=request.user,
                author__icontains=query
            )
    
    return render(request, 'bookshelf/book_search.html', {
        'books': books,
        'query': query
    })
