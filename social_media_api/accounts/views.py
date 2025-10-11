from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, FollowSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class CustomObtainAuthToken(ObtainAuthToken):
    """
    Custom login view that returns user data along with token.
    """
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating user profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, username):
    """
    Follow or unfollow a user.
    """
    user_to_follow = get_object_or_404(User, username=username)
    
    if user_to_follow == request.user:
        return Response({
            'error': 'You cannot follow yourself'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = FollowSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    action = serializer.validated_data['action']
    
    if action == 'follow':
        if request.user.following.filter(id=user_to_follow.id).exists():
            return Response({
                'message': 'You are already following this user'
            }, status=status.HTTP_200_OK)
        
        request.user.following.add(user_to_follow)
        
        # Create notification (we'll implement this in Task 3)
        from notifications.models import Notification
        Notification.objects.create(
            recipient=user_to_follow,
            actor=request.user,
            verb='followed you',
            target=user_to_follow
        )
        
        return Response({
            'message': f'You are now following {user_to_follow.username}'
        }, status=status.HTTP_200_OK)
    
    elif action == 'unfollow':
        if not request.user.following.filter(id=user_to_follow.id).exists():
            return Response({
                'message': 'You are not following this user'
            }, status=status.HTTP_200_OK)
        
        request.user.following.remove(user_to_follow)
        return Response({
            'message': f'You have unfollowed {user_to_follow.username}'
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    """
    Get list of all users (for discovery).
    """
    users = User.objects.exclude(id=request.user.id)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
