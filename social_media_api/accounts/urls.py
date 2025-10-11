from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomObtainAuthToken.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('users/', views.user_list, name='user_list'),
    path('<str:username>/follow/', views.follow_user, name='follow_user'),
]