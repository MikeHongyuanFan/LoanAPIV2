from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime

from .models import Application, Note
from .serializers import NoteSerializer
from apps.authentication.permissions import IsStaff


class NoteListView(generics.ListAPIView):
    """
    API endpoint for listing notes for an application.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        application_id = self.kwargs.get('pk')
        return Note.objects.filter(application_id=application_id).order_by('-created_at')


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a note.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        application_id = self.kwargs.get('pk')
        return Note.objects.filter(application_id=application_id)


class NoteReminderView(APIView):
    """
    API endpoint for managing note reminders.
    """
    permission_classes = [IsAuthenticated, IsStaff]
    
    def post(self, request, pk, note_id):
        try:
            note = Note.objects.get(id=note_id, application_id=pk)
            
            # Get reminder date from request
            remind_date_str = request.data.get('remind_date')
            if not remind_date_str:
                return Response({
                    'error': 'Reminder date is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Parse reminder date
            try:
                remind_date = datetime.strptime(remind_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({
                    'error': 'Invalid date format. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update note with reminder date
            note.remind_date = remind_date
            note.save()
            
            return Response({
                'message': f'Reminder set for {remind_date}',
                'note_id': note.id,
                'remind_date': remind_date
            })
            
        except Note.DoesNotExist:
            return Response({
                'error': 'Note not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk, note_id):
        try:
            note = Note.objects.get(id=note_id, application_id=pk)
            
            # Remove reminder
            note.remind_date = None
            note.save()
            
            return Response({
                'message': 'Reminder removed',
                'note_id': note.id
            })
            
        except Note.DoesNotExist:
            return Response({
                'error': 'Note not found'
            }, status=status.HTTP_404_NOT_FOUND)


class PendingRemindersView(APIView):
    """
    API endpoint for retrieving pending reminders.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get current date
        today = timezone.now().date()
        
        # Get notes with reminders due today or in the past
        reminders = Note.objects.filter(
            remind_date__lte=today,
            reminder_sent=False
        ).select_related('application', 'created_by')
        
        # Format response
        reminder_data = []
        for note in reminders:
            reminder_data.append({
                'id': note.id,
                'content': note.content,
                'created_at': note.created_at,
                'remind_date': note.remind_date,
                'days_overdue': (today - note.remind_date).days,
                'application': {
                    'id': note.application.id,
                    'reference_number': note.application.reference_number
                },
                'created_by': note.created_by.user.username if note.created_by and note.created_by.user else None
            })
        
        return Response({
            'count': len(reminder_data),
            'reminders': reminder_data
        })


class ProcessRemindersView(APIView):
    """
    API endpoint for processing pending reminders.
    """
    permission_classes = [IsAuthenticated, IsStaff]
    
    def post(self, request):
        # Get current date
        today = timezone.now().date()
        
        # Get notes with reminders due today or in the past
        reminders = Note.objects.filter(
            remind_date__lte=today,
            reminder_sent=False
        ).select_related('application', 'created_by')
        
        # Process reminders
        processed_count = 0
        for note in reminders:
            # In a real implementation, this would send notifications
            # For now, just mark as sent
            note.reminder_sent = True
            note.save()
            processed_count += 1
        
        return Response({
            'message': f'Processed {processed_count} reminders',
            'processed_count': processed_count
        })
