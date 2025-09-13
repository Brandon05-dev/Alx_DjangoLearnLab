"""
URL configuration for the bookshelf app.

Security considerations:
- Uses specific URL patterns to prevent unauthorized access
- Includes CSRF protection where needed
- Implements proper HTTP method restrictions
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Book management URLs
    path('books/', views.book_list, name='book-list'),
    path('books/create/', views.create_book, name='book-create'),
    path('books/<int:book_id>/', views.SecureBookDetailView.as_view(), name='book-detail'),
    path('books/<int:book_id>/edit/', views.edit_book, name='book-edit'),
    path('books/<int:book_id>/delete/', views.delete_book, name='book-delete'),
    
    # API endpoints
    path('api/books/search/', views.book_search_api, name='book-search-api'),
    
    # Authentication URLs (using Django's built-in views for security)
    path('login/', auth_views.LoginView.as_view(template_name='bookshelf/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='bookshelf/password_change.html',
        success_url='/password-change/done/'
    ), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='bookshelf/password_change_done.html'
    ), name='password_change_done'),
]
