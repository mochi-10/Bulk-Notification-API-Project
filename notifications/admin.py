from django.contrib import admin
from .models import Sender, Notification
# Register your models here.



@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']
    search_fields = ['name', 'email']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'channel', 'sender_id']
    list_filter = ['channel']
    search_fields = ['title', 'message']