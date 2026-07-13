from rest_framework import serializers
from .models import Sender, Notification

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'channel']
    
    def validate_channel(self, value):
        """Validate that channel is one of the allowed choices"""
        allowed_channels = ['email', 'sms', 'push']
        if value not in allowed_channels:
            raise serializers.ValidationError(
                f"Channel must be one of: {', '.join(allowed_channels)}"
            )
        return value
    
    def validate_title(self, value):
        """Validate title is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip()
    
    def validate_message(self, value):
        """Validate message is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        return value.strip()


class BulkNotificationSerializer(serializers.Serializer):
    """Serializer for bulk notification request"""
    
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    notifications = serializers.ListField(
        child=NotificationSerializer(),
        min_length=1,
        max_length=100
    )
    
    def validate(self, data):
        """Cross-field validation"""
        # Validate name is not empty
        if not data.get('name') or not data.get('name').strip():
            raise serializers.ValidationError(
                {"name": "Name cannot be empty"}
            )
        
        # Validate email format
        email = data.get('email', '')
        if '@' not in email:
            raise serializers.ValidationError(
                {"email": "Invalid email format"}
            )
        
        # Validate notifications list is not empty
        if not data.get('notifications'):
            raise serializers.ValidationError(
                {"notifications": "At least one notification is required"}
            )
        
        # Check for duplicate notification titles
        titles = [n.get('title', '').lower() for n in data.get('notifications', [])]
        if len(titles) != len(set(titles)):
            raise serializers.ValidationError(
                {"notifications": "Duplicate notification titles are not allowed"}
            )
        
        return data