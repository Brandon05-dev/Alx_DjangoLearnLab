from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .models import Book, Library, Author, UserProfile
from django.contrib.auth.models import User


# Task 1: Function-based view to list all books
def list_books(request):
    """Function-based view: list all books with authors."""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Task 1: Class-based view for library detail
class LibraryDetailView(DetailView):
    """Class-based view: library detail view with books."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# Task 2: User Authentication Views
def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


class CustomLoginView(LoginView):
    """Custom login view."""
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    template_name = 'relationship_app/logout.html'


# Task 3: Role-based Access Control Functions
def is_admin(user):
    """Check if user is admin."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'


def is_librarian(user):
    """Check if user is librarian."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'


def is_member(user):
    """Check if user is member."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# Task 3: Role-based Views
@user_passes_test(is_admin)
def admin_view(request):
    """Admin-only view."""
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian-only view."""
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    """Member-only view."""
    return render(request, 'relationship_app/member_view.html')


# Task 4: Custom Permissions Views
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """Add book view with custom permission."""
    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        if title and author_name:
            author, created = Author.objects.get_or_create(name=author_name)
            Book.objects.create(title=title, author=author)
            messages.success(request, 'Book added successfully!')
            return redirect('list_books')
    return render(request, 'relationship_app/add_book.html')


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """Edit book view with custom permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        if title and author_name:
            book.title = title
            author, created = Author.objects.get_or_create(name=author_name)
            book.author = author
            book.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('list_books')
    return render(request, 'relationship_app/edit_book.html', {'book': book})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """Delete book view with custom permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
