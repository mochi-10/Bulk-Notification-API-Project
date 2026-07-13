from django.shortcuts import render
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Sender, Notification
from .serializers import BulkNotificationSerializer, NotificationSerializer

class BulkNotificationCreateView(APIView):
    """
    API View to create a sender and multiple notifications in bulk
    POST /api/notifications/bulk/
    """
    
    def post(self, request, *args, **kwargs):
        
        serializer = BulkNotificationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        try:
            # Step 2: Use transaction atomicity for data integrity
            with transaction.atomic():
                # Create the sender
                sender = Sender.objects.create(
                    name=validated_data['name'],
                    email=validated_data['email']
                )
                
                # Step 3: Prepare notifications for bulk_create
                notifications_to_create = []
                for notif_data in validated_data['notifications']:
                    notification = Notification(
                        title=notif_data['title'],
                        message=notif_data['message'],
                        channel=notif_data['channel'],
                        sender=sender
                    )
                    notifications_to_create.append(notification)
                
                
                created_notifications = Notification.objects.bulk_create(
                    notifications_to_create
                )
                
              
                notification_ids = [n.id for n in created_notifications]
                
               
                created_notifications_with_ids = Notification.objects.filter(
                    id__in=notification_ids
                )
                
                
                notification_serializer = NotificationSerializer(
                    created_notifications_with_ids,  
                    many=True
                )
                
                return Response({
                    'success': True,
                    'message': f'Successfully created {len(created_notifications)} notification(s)',
                    'data': {
                        'sender': {
                            'id': sender.id,
                            'name': sender.name,
                            'email': sender.email
                        },
                        'notifications': notification_serializer.data,
                        'total_count': len(created_notifications)
                    }
                }, status=status.HTTP_201_CREATED)
                
        except IntegrityError as e:
            return Response({
                'success': False,
                'error': 'Database integrity error occurred',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'success': False,
                'error': 'An unexpected error occurred',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HealthCheckView(APIView):
    """Simple health check endpoint"""
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'service': 'Bulk Notification API'
        }, status=status.HTTP_200_OK)