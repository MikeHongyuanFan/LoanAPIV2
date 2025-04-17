#!/usr/bin/env python
"""
Script to set up a test database for the Loan Application System.
This creates a separate SQLite database for testing purposes.
"""

import os
import sys
import django
from django.core.management import call_command

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.test_settings')
os.environ.setdefault('DB_TYPE', 'test')

def setup_test_database():
    """Set up a test database with initial data."""
    print("Setting up test database...")
    
    # Initialize Django
    django.setup()
    
    # Run migrations
    call_command('makemigrations')
    call_command('migrate')
    
    # Create a superuser for testing
    from django.contrib.auth.models import User
    if not User.objects.filter(username='testadmin').exists():
        User.objects.create_superuser(
            username='testadmin',
            email='testadmin@example.com',
            password='testpassword'
        )
        print("Created test superuser: testadmin / testpassword")
    
    # Load any test fixtures if needed
    # call_command('loaddata', 'test_data.json')
    
    print("Test database setup complete!")

if __name__ == '__main__':
    setup_test_database()
