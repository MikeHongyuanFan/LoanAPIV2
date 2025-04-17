#!/bin/bash

# Script to run tests for the Loan Application System

# Set environment variables for testing
export DJANGO_SETTINGS_MODULE=tests.test_settings
export DB_TYPE=test

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up test environment...${NC}"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies if needed
pip install -r requirements.txt

# Setup test database
python setup_test_db.py

echo -e "${YELLOW}Running unit tests...${NC}"
python -m pytest tests/unit -v

echo -e "${YELLOW}Running integration tests...${NC}"
python -m pytest tests/integration -v

echo -e "${YELLOW}Running functional tests...${NC}"
python -m pytest tests/functional -v

echo -e "${YELLOW}Running coverage report...${NC}"
coverage run --source='.' -m pytest
coverage report
coverage html

echo -e "${GREEN}All tests completed!${NC}"
echo -e "${YELLOW}View detailed coverage report by opening htmlcov/index.html in your browser${NC}"
