"""
Database configuration for the Loan Application System.
This file contains settings for different environments (development, testing, production).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Default SQLite configuration
SQLITE_CONFIG = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

# PostgreSQL configuration
POSTGRES_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ.get('DB_NAME', 'loan_application'),
    'USER': os.environ.get('DB_USER', 'postgres'),
    'PASSWORD': os.environ.get('DB_PASSWORD', ''),
    'HOST': os.environ.get('DB_HOST', 'localhost'),
    'PORT': os.environ.get('DB_PORT', '5432'),
}

# Test database configuration
TEST_CONFIG = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'test_db.sqlite3',
}

# Choose database based on environment
def get_database_config():
    """
    Return the appropriate database configuration based on environment variables.
    """
    db_type = os.environ.get('DB_TYPE', 'sqlite').lower()
    
    if db_type == 'postgres':
        return POSTGRES_CONFIG
    elif db_type == 'test':
        return TEST_CONFIG
    else:
        return SQLITE_CONFIG
