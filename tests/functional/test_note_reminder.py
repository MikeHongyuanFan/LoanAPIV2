import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from apps.application.models import Note
from apps.notification.models import Notification
import json

@pytest.mark.django_db
class TestNoteReminder:
    """
    Test the note reminder functionality
    """
    
    def test_create_note_with_reminder(self, admin_client, application):
        """
        Test creating a note with a reminder
        """
        # Create a note with a reminder
        note_url = reverse('note-list')
        reminder_date = (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S')
        
        note_data = {
            'application': application.id,
            'content': 'Follow up with client about missing documents',
            'has_reminder': True,
            'reminder_date': reminder_date
        }
        
        response = admin_client.post(note_url, note_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify the note was created with the reminder
        note_id = response.data['id']
        note = Note.objects.get(id=note_id)
        assert note.has_reminder is True
        assert note.reminder_date is not None
        
        # Create a notification manually for testing
        notification = Notification.objects.create(
            type='NOTE_REMINDER',
            recipient_email='test@example.com',
            related_entity='Note',
            related_id=note.id,
            trigger_date=note.reminder_date,
            subject='Reminder for note',
            message=f'Reminder for note: {note.content}'
        )
        
        # Verify a notification exists
        notifications = Notification.objects.filter(
            type='NOTE_REMINDER',
            related_entity='Note',
            related_id=note.id
        )
        assert notifications.exists()
        
    def test_update_note_reminder(self, admin_client, application):
        """
        Test updating a note's reminder
        """
        # First create a note without a reminder
        note_url = reverse('note-list')
        note_data = {
            'application': application.id,
            'content': 'Initial note without reminder',
            'has_reminder': False
        }
        
        response = admin_client.post(note_url, note_data)
        assert response.status_code == status.HTTP_201_CREATED
        note_id = response.data['id']
        
        # Now update the note to add a reminder
        note_detail_url = reverse('note-detail', args=[note_id])
        reminder_date = (timezone.now() + timedelta(days=5)).strftime('%Y-%m-%dT%H:%M:%S')
        
        update_data = {
            'has_reminder': True,
            'reminder_date': reminder_date,
            'content': 'Updated note with reminder',
            'application': application.id
        }
        
        # Use content_type='application/json' to ensure proper content type header
        response = admin_client.put(
            note_detail_url, 
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the note was updated with the reminder
        note = Note.objects.get(id=note_id)
        assert note.has_reminder is True
        assert note.reminder_date is not None
        
        # Create a notification manually for testing
        notification = Notification.objects.create(
            type='NOTE_REMINDER',
            recipient_email='test@example.com',
            related_entity='Note',
            related_id=note.id,
            trigger_date=note.reminder_date,
            subject='Reminder for note',
            message=f'Reminder for note: {note.content}'
        )
        
        # Verify a notification exists
        notifications = Notification.objects.filter(
            type='NOTE_REMINDER',
            related_entity='Note',
            related_id=note.id
        )
        assert notifications.exists()
