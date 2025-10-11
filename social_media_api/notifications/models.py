from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Notification(models.Model):
    """
    Model representing notifications for users.
    """
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        help_text="The user who will receive this notification"
    )
    actor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_notifications',
        help_text="The user who triggered this notification"
    )
    verb = models.CharField(
        max_length=255,
        help_text="Description of the action (e.g., 'liked your post', 'followed you')"
    )
    target_content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Content type of the target object"
    )
    target_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="ID of the target object"
    )
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(
        default=False,
        help_text="Whether the notification has been read"
    )

    class Meta:
        ordering = ['-timestamp']
        db_table = 'notifications_notification'
        indexes = [
            models.Index(fields=['recipient', 'read']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.actor.username} {self.verb} for {self.recipient.username}"

    def mark_as_read(self):
        """Mark this notification as read"""
        if not self.read:
            self.read = True
            self.save(update_fields=['read'])

    @classmethod
    def mark_all_as_read(cls, user):
        """Mark all notifications for a user as read"""
        return cls.objects.filter(recipient=user, read=False).update(read=True)
