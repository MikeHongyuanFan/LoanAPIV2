# Database Configuration and Testing Setup

This document outlines the database configuration and testing setup for the Loan Application System V2.

## Database Configuration

The system is configured to support multiple database backends:

1. **SQLite** (default for development)
2. **PostgreSQL** (recommended for production)
3. **In-memory SQLite** (for testing)

### Configuration Files

- `loan_project/database_settings.py` - Contains database configuration options
- `.env` - Environment variables for database connection settings

### Switching Database Backends

To switch between database backends, modify the `DB_TYPE` variable in the `.env` file:

```
# For SQLite (default)
DB_TYPE=sqlite

# For PostgreSQL
DB_TYPE=postgres
DB_NAME=loan_application
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# For testing
DB_TYPE=test
```

## Testing Setup

The project is configured with a comprehensive testing framework:

### Test Structure

- `tests/unit/` - Unit tests for individual components
- `tests/integration/` - Integration tests for API endpoints
- `tests/functional/` - Functional tests for complete workflows

### Test Configuration

- `tests/test_settings.py` - Django settings specific to testing
- `pytest.ini` - Configuration for pytest
- `setup_test_db.py` - Script to set up a test database
- `run_tests.sh` - Shell script to run all tests with coverage

### Running Tests

To run all tests with coverage:

```bash
./run_tests.sh
```

To run specific test categories:

```bash
# Run unit tests only
python -m pytest tests/unit -v

# Run integration tests only
python -m pytest tests/integration -v

# Run functional tests only
python -m pytest tests/functional -v
```

### Test Fixtures

Common test fixtures are defined in `tests/conftest.py`, including:

- API clients (anonymous, regular user, staff, admin)
- User accounts with different permission levels
- Sample data for borrowers, brokers, products, etc.

## Next Steps

1. Run migrations to create the database schema
2. Create a superuser for admin access
3. Run the test suite to verify the setup
4. Start the development server
