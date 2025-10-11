from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsAuthorOrReadOnly

User = get_user_model()


class PostListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating posts.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related('comments', 'likes')


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting individual posts.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related('comments', 'likes')


class CommentListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating comments for a specific post.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).select_related('author', 'post')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        comment = serializer.save(post=post)
        
        # Create notification for post author (if not self-comment)
        if post.author != self.request.user:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb='commented on your post',
                target=post
            )


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting individual comments.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.select_related('author', 'post')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
    """
    Like or unlike a post.
    """
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    try:
        like = Like.objects.get(user=user, post=post)
        like.delete()
        message = 'Post unliked successfully'
        liked = False
    except Like.DoesNotExist:
        Like.objects.create(user=user, post=post)
        message = 'Post liked successfully'
        liked = True
        
        # Create notification for post author (if not self-like)
        if post.author != user:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked your post',
                target=post
            )
    
    return Response({
        'message': message,
        'liked': liked,
        'likes_count': post.likes_count
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    """
    Get posts from users that the current user follows.
    """
    user = request.user
    # Get posts from users that the current user follows
    following_users = user.following.all()
    posts = Post.objects.filter(author__in=following_users).select_related('author').prefetch_related('comments', 'likes').order_by('-created_at')
    
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
