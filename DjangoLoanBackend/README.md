# Loan Application System V2

A comprehensive CRM system for managing loan applications, borrowers, brokers, and related services built with Django.

## Project Overview

This system provides a complete solution for loan management, including:

- Application processing and tracking
- Borrower and guarantor management
- Broker and referral tracking
- Document generation and management
- Notification system for repayments and status changes
- User authentication and permission management

## System Architecture

The system is built using Django with a modular app structure:

1. **Application App** - Core loan application management
2. **Borrower App** - Borrower information management
3. **Guarantor App** - Guarantor information management
4. **Broker App** - Broker and referral management
5. **Valuer App** - Property valuation management
6. **QS App** - Quantity surveyor management
7. **Product App** - Loan product management
8. **Authentication App** - User management and security
9. **Notification App** - Email and system notifications
10. **Document App** - Document generation and storage

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Installation

1. Clone the repository:
   ```
   git clone [repository-url]
   cd LoanApplicationV2
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your specific configuration.

5. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```
   python manage.py runserver
   ```

### API Documentation

API documentation is available at `/api/docs/` when the server is running.

## Project Structure

```
LoanApplicationV2/
├── loan_project/              # Django project settings
├── apps/                      # Django applications
│   ├── application/           # Loan application management
│   ├── borrower/              # Borrower management
│   ├── broker/                # Broker management
│   ├── document/              # Document management
│   ├── notification/          # Notification system
│   └── ...                    # Other apps
├── templates/                 # HTML templates
├── static/                    # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── media/                     # User-uploaded files
├── manage.py                  # Django management script
├── requirements.txt           # Project dependencies
└── .env                       # Environment variables
```

## Development Roadmap

1. Core API development
2. Frontend templates and views
3. Integration testing
4. User acceptance testing
5. Deployment

## License

[License information]
