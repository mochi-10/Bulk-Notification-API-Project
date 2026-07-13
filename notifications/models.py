from django.db import models

# Create your models here.


class Sender(models.Model):
    """Model for notification senders"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    
    
    class Meta:
        db_table = 'sender'
    
    def __str__(self):
        return f"{self.name} ({self.email})"


class Notification(models.Model):
    """Model for notifications"""
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push'),
    ]
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    sender = models.ForeignKey(
        Sender, 
        on_delete=models.CASCADE,
        db_column='sender_id'  # Explicitly set the foreign key column name
    )
    
    class Meta:
        db_table = 'notification'
    
    def __str__(self):
        return f"{self.title} - {self.channel}"