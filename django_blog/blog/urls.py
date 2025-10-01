from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('posts/<int:post_id>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', views.update_comment, name='update-comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete-comment'),
    path('comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('search/', views.search_posts, name='search-posts'),
    path('tags/<str:tag_name>/', views.PostByTagListView.as_view(), name='posts-by-tag'),
]