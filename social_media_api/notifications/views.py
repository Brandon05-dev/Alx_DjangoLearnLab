from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    View for listing user's notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related('actor', 'target_content_type')


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    """
    Mark a specific notification as read.
    """
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        recipient=request.user
    )
    
    notification.mark_as_read()
    
    return Response({
        'message': 'Notification marked as read',
        'notification': NotificationSerializer(notification).data
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """
    Mark all notifications as read for the current user.
    """
    count = Notification.mark_all_as_read(request.user)
    
    return Response({
        'message': f'{count} notifications marked as read'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_notifications_count(request):
    """
    Get count of unread notifications for the current user.
    """
    count = Notification.objects.filter(
        recipient=request.user, 
        read=False
    ).count()
    
    return Response({
        'unread_count': count
    }, status=status.HTTP_200_OK)
