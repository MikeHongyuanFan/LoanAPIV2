# Implementation Gaps and API Service Matrix

This document provides a comprehensive overview of the implemented API services in the Loan Application System V2 and identifies gaps that need to be addressed in future development iterations.

## API Service Implementation Matrix

| Service | Core Endpoints | Related Endpoints | Status | Notes |
|---------|---------------|-------------------|--------|-------|
| **Application Service** | GET /applications/<br>GET /applications/{id}/<br>POST /applications/<br>DELETE /applications/{id}/<br>PATCH /applications/{id}/ | POST /applications/{id}/documents/<br>POST /applications/{id}/generate-documents/<br>POST /applications/{id}/notes/<br>POST /applications/{id}/calculator/<br>POST /applications/{id}/repayments/<br>POST /applications/{id}/extension/ | ✅ Implemented | Missing duplicate application functionality |
| **Borrower Service** | GET /borrowers/<br>GET /borrowers/{id}/<br>POST /borrowers/ | GET /borrowers/search/<br>GET /borrowers/{id}/applications/ | ✅ Implemented | Missing duplicate detection logic |
| **Guarantor Service** | POST /guarantors/<br>GET /guarantors/{id}/ | - | ✅ Implemented | - |
| **Broker Service** | GET /brokers/<br>GET /brokers/{id}/<br>POST /brokers/<br>DELETE /brokers/{id}/ | GET /brokers/{id}/applications/<br>GET /brokers/{id}/borrowers/ | ✅ Implemented | Missing commission account tracking |
| **Valuer Service** | GET /valuers/<br>POST /valuers/<br>DELETE /valuers/{id}/<br>GET /valuers/{id}/applications/ | - | ✅ Implemented | - |
| **QS Service** | GET /qs/<br>POST /qs/<br>DELETE /qs/{id}/<br>GET /qs/{id}/applications/ | - | ✅ Implemented | - |
| **Product Service** | GET /products/<br>GET /products/{id}/<br>GET /products/{id}/documents/ | - | ✅ Implemented | - |
| **Authentication Service** | POST /auth/login/<br>POST /auth/forgot-password/<br>POST /auth/change-password/<br>POST /auth/create-account/<br>DELETE /auth/delete-account/ | - | ✅ Implemented | Needs comprehensive permission system |
| **Notification Service** | - | - | ⚠️ Partially Implemented | Missing automatic triggers |
| **Document Service** | POST /documents/generate/<br>GET /documents/{id}/<br>POST /documents/upload/ | - | ⚠️ Partially Implemented | Missing DocuSign integration and template-based generation |

## Implementation Gaps

### 1. Application Service
- **Duplicate Application Functionality**: 
  - No endpoint or method to clone an existing application with its related data
  - Required for streamlining repeat business from the same borrower

- **Fee Management System**:
  - Missing functionality to track fee status (paid/waiting)
  - No invoice upload capability for fees
  - No ledger system for tracking payments received/made

- **Stage Change Notifications**:
  - While models exist, automatic email notifications on stage changes are not implemented
  - Missing integration with notification service for stage stagnation alerts

### 2. Document Service
- **DocuSign Integration**:
  - No integration with DocuSign for electronic document signing
  - Missing functionality to send generated documents to borrowers via DocuSign

- **Template-based Document Generation**:
  - Basic document generation exists but lacks support for different templates
  - Missing templates for different recipients (solicitor, client, internal accountant)

### 3. Notification Service
- **Automatic Triggers**:
  - Missing scheduled jobs or event listeners for:
    - Repayment reminders (X days before due date)
    - Loan expiration reminders
    - Late repayment notifications (3, 7, 10 days after due date)
    - Stage stagnation alerts
    - Note reminders on specified dates

- **Notification Preferences**:
  - While settings endpoints exist, the actual application of these preferences to notification delivery is not implemented

### 4. Permission System
- **Role-based Access Control**:
  - Basic roles defined but comprehensive permissions not implemented across all endpoints
  - Missing "Admin only with 100% full access" implementation
  - No granular permission checks on sensitive operations

### 5. Borrower Service
- **Duplicate Detection**:
  - Missing logic to identify borrowers with the same name, DOB, and email address
  - No functionality to merge or link potential duplicate records

### 6. Repayment Management
- **Invoice Upload for Repayments**:
  - No specific functionality to upload invoices for repayments
  - Missing integration with document service for invoice storage

- **Automatic Reminders**:
  - Missing scheduled jobs for automatic repayment reminders
  - No integration with notification service for repayment alerts

### 7. Broker Service
- **Commission Account**:
  - Missing commission tracking system for brokers
  - No endpoints for managing commission payments
  - No reporting functionality for commission accounts

### 8. Integration Between Services
- **Event-driven Communication**:
  - Missing event listeners and hooks for inter-service communication
  - No automatic triggering of notifications based on events in other services

## Priority Implementation Recommendations

1. **High Priority**:
   - Automatic notification triggers for critical events
   - Fee management system with payment tracking
   - Comprehensive permission system
   - Stage change notifications

2. **Medium Priority**:
   - DocuSign integration
   - Duplicate application functionality
   - Broker commission tracking
   - Borrower duplicate detection

3. **Lower Priority**:
   - Template-based document generation enhancements
   - Advanced reporting features
   - Integration optimizations

## Technical Approach for Addressing Gaps

### For Automatic Triggers:
```python
# Example implementation for scheduled notification triggers
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.application.models import Application
from apps.notification.models import Notification

@receiver(post_save, sender=Application)
def application_stage_changed(sender, instance, created, **kwargs):
    if not created and instance.tracker.has_changed('stage'):
        # Create notification for stage change
        Notification.objects.create(
            type='STAGE_CHANGE',
            recipient_email=instance.broker.email,
            related_id=instance.id,
            subject=f"Application {instance.id} Stage Changed",
            message=f"The application has moved to {instance.get_stage_display()} stage."
        )
```

### For Fee Management:
```python
# Example model extension for fee tracking
class Fee(models.Model):
    STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('WAITING', 'Waiting Payment'),
    ]
    
    application = models.ForeignKey('Application', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='WAITING')
    invoice = models.FileField(upload_to='invoices/', null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
```

### For Permission System:
```python
# Example permission check in a view
from rest_framework.permissions import BasePermission

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role in ['ADMIN', 'MANAGER']
        
# Apply to views
class SensitiveOperationView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]
```

## Conclusion

While the Loan Application System V2 has a solid foundation with most API endpoints implemented, several key functional areas require further development to meet all the requirements specified in the documentation. The gaps identified in this document should be addressed in the next development phase to ensure a complete and robust system.
