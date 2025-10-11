from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    """
    actor = UserSerializer(read_only=True)
    target_type = serializers.SerializerMethodField()
    target_title = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'verb', 'target_type', 
            'target_title', 'timestamp', 'read'
        ]
        read_only_fields = ['id', 'recipient', 'actor', 'verb', 'timestamp']

    def get_target_type(self, obj):
        """Get the type of the target object"""
        if obj.target:
            return obj.target_content_type.model
        return None

    def get_target_title(self, obj):
        """Get a string representation of the target object"""
        if obj.target:
            if hasattr(obj.target, 'content'):
                # For Post objects
                return obj.target.content[:50] + '...' if len(obj.target.content) > 50 else obj.target.content
            elif hasattr(obj.target, 'username'):
                # For User objects (follow notifications)
                return obj.target.username
            else:
                return str(obj.target)
        return None