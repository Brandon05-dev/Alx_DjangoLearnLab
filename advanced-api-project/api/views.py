from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer


# Custom permission class for role-based access
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their own books.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author of the book
        return obj.author == request.user


class BookListView(generics.ListAPIView):
    """
    Generic ListView for retrieving all books with advanced query capabilities.
    
    This view handles GET requests to retrieve a list of all books in the database.
    Uses Django REST Framework's ListAPIView which provides read-only access
    to a collection of model instances.
    
    Advanced Features:
    - Filtering: Filter books by title, author, and publication_year
    - Searching: Search books by title and author name  
    - Ordering: Order books by title and publication_year
    
    Query Examples:
    - /api/books/?title=Django  (filter by title)
    - /api/books/?author=1  (filter by author ID)
    - /api/books/?publication_year=2023  (filter by publication year)
    - /api/books/?search=python  (search in title and author name)
    - /api/books/?ordering=title  (order by title ascending)
    - /api/books/?ordering=-publication_year  (order by publication year descending)
    
    Permissions: 
    - Allows read access to both authenticated and unauthenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow read access to all users
    
    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Configure filtering fields
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Configure search fields
    search_fields = ['title', 'author__name']
    
    # Configure ordering fields
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for retrieving a single book by ID.
    
    This view handles GET requests to retrieve a specific book instance
    identified by its primary key (ID). Uses Django REST Framework's
    RetrieveAPIView for read-only access to individual model instances.
    
    Permissions:
    - Allows read access to both authenticated and unauthenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow read access to all users


class BookCreateView(generics.CreateAPIView):
    """
    Generic CreateView for adding a new book.
    
    This view handles POST requests to create new book instances.
    Uses Django REST Framework's CreateAPIView which provides
    create-only endpoints for model instances.
    
    Custom behavior:
    - Includes data validation through the BookSerializer
    - Automatically handles form submission and data validation
    
    Permissions:
    - Restricted to authenticated users only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create


class BookUpdateView(generics.UpdateAPIView):
    """
    Generic UpdateView for modifying an existing book.
    
    This view handles PUT and PATCH requests to update existing book instances.
    Uses Django REST Framework's UpdateAPIView which provides
    update-only endpoints for model instances.
    
    Custom behavior:
    - Properly handles partial updates (PATCH) and full updates (PUT)
    - Includes data validation through the BookSerializer
    - Automatically handles form submissions and data validation
    
    Permissions:
    - Restricted to authenticated users with role-based access
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]  # Role-based permissions


class BookDeleteView(generics.DestroyAPIView):
    """
    Generic DeleteView for removing a book.
    
    This view handles DELETE requests to remove existing book instances.
    Uses Django REST Framework's DestroyAPIView which provides
    delete-only endpoints for model instances.
    
    Permissions:
    - Restricted to authenticated users with role-based access
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]  # Role-based permissions
