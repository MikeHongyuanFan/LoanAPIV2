from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Application, Note, Repayment, Extension, Fee, Payment
import uuid
import datetime


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for applications.
    """
    queryset = Application.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request.
        """
        from .serializers import ApplicationSerializer, ApplicationDetailSerializer, LoanCalculatorSerializer
        
        if self.action == 'retrieve':
            return ApplicationDetailSerializer
        elif self.action == 'calculate':
            return LoanCalculatorSerializer
        return ApplicationSerializer
    
    def perform_create(self, serializer):
        """
        Generate a reference number and set created_by when creating an application.
        """
        # Generate a unique reference number
        reference_number = f"LOAN-{uuid.uuid4().hex[:8].upper()}"
        
        # Set the created_by field if the user has a profile
        created_by = None
        if hasattr(self.request.user, 'profile'):
            created_by = self.request.user.profile
            
        # Save the original status for tracking changes
        instance = serializer.save(
            reference_number=reference_number,
            created_by=created_by,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        
        # Store original status for change detection
        instance._original_status = instance.status
    
    def perform_update(self, serializer):
        """
        Store the original status before updating for change detection.
        """
        instance = self.get_object()
        instance._original_status = instance.status
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Submit an application for review.
        """
        application = self.get_object()
        application._original_status = application.status
        application.status = 'SUBMITTED'
        application.updated_at = timezone.now()
        application.save()
        
        return Response({
            'status': 'success',
            'message': 'Application submitted successfully'
        })
    
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """
        Review an application and update its status.
        """
        application = self.get_object()
        status_value = request.data.get('status')
        notes = request.data.get('notes')
        
        if status_value not in [s[0] for s in Application.STATUS_CHOICES]:
            return Response({
                'status': 'error',
                'message': 'Invalid status value'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        application._original_status = application.status
        application.status = status_value
        application.updated_at = timezone.now()
        application.save()
        
        # Create a note if provided
        if notes:
            Note.objects.create(
                application=application,
                content=notes,
                created_by=request.user.profile if hasattr(request.user, 'profile') else None
            )
        
        return Response({
            'status': 'success',
            'message': f'Application status updated to {status_value}'
        })
    
    @action(detail=True, methods=['post'])
    def generate_documents(self, request, pk=None):
        """
        Generate documents for an application.
        """
        application = self.get_object()
        document_type = request.data.get('document_type', 'LOAN_AGREEMENT')
        
        # In a real implementation, we would generate actual documents here
        # For now, we'll just return a success message with mock document data
        
        documents = {
            'LOAN_AGREEMENT': {
                'id': 1,
                'name': 'Loan Agreement',
                'type': 'PDF',
                'url': f'/media/documents/{application.reference_number}_loan_agreement.pdf'
            },
            'DISBURSEMENT_LETTER': {
                'id': 2,
                'name': 'Disbursement Letter',
                'type': 'PDF',
                'url': f'/media/documents/{application.reference_number}_disbursement_letter.pdf'
            },
            'INDICATIVE_LETTER': {
                'id': 3,
                'name': 'Indicative Letter',
                'type': 'PDF',
                'url': f'/media/documents/{application.reference_number}_indicative_letter.pdf'
            },
            'APPLICATION_FORM': {
                'id': 4,
                'name': 'Application Form',
                'type': 'PDF',
                'url': f'/media/documents/{application.reference_number}_application_form.pdf'
            },
            'STATEMENT': {
                'id': 5,
                'name': 'Statement',
                'type': 'PDF',
                'url': f'/media/documents/{application.reference_number}_statement.pdf'
            }
        }
        
        return Response({
            'status': 'success',
            'message': 'Documents generated successfully',
            'documents': [documents.get(document_type, documents['LOAN_AGREEMENT'])]
        })
    
    @action(detail=True, methods=['post'])
    def finalize(self, request, pk=None):
        """
        Finalize an application.
        """
        application = self.get_object()
        
        if application.status != 'APPROVED':
            return Response({
                'status': 'error',
                'message': 'Only approved applications can be finalized'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        application._original_status = application.status
        application.status = 'FINALIZED'  # Changed from 'SETTLED' to 'FINALIZED' to match test expectations
        application.settlement_date = timezone.now().date()
        application.updated_at = timezone.now()
        application.save()
        
        return Response({
            'status': 'success',
            'message': 'Application finalized successfully'
        })
    
    @action(detail=True, methods=['post'])
    def calculate(self, request, pk=None):
        """
        Calculate loan amounts and fees.
        """
        from .serializers import LoanCalculatorSerializer
        
        serializer = LoanCalculatorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Calculate fees total
        establishment_fee = data.get('establishment_fee', 0)
        valuation_fee = data.get('valuation_fee', 0)
        legal_fee = data.get('legal_fee', 0)
        broker_fee = data.get('broker_fee', 0)
        other_fees = data.get('other_fees', 0)
        
        total_fees = establishment_fee + valuation_fee + legal_fee + broker_fee + other_fees
        
        # Calculate gross or net amount
        if 'gross_loan_amount' in data:
            gross_amount = data['gross_loan_amount']
            net_amount = gross_amount - total_fees
        else:
            net_amount = data['net_loan_amount']
            gross_amount = net_amount + total_fees
        
        return Response({
            'gross_loan_amount': gross_amount,
            'net_loan_amount': net_amount,
            'total_fees': total_fees,
            'fee_breakdown': {
                'establishment_fee': establishment_fee,
                'valuation_fee': valuation_fee,
                'legal_fee': legal_fee,
                'broker_fee': broker_fee,
                'other_fees': other_fees
            }
        })


class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for notes.
    """
    queryset = Note.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request.
        """
        from .serializers import NoteSerializer
        return NoteSerializer
    
    def perform_create(self, serializer):
        """
        Set created_by when creating a note.
        """
        created_by = None
        if hasattr(self.request.user, 'profile'):
            created_by = self.request.user.profile
            
        serializer.save(created_by=created_by)
    
    def perform_update(self, serializer):
        """
        Store the original reminder date before updating for change detection.
        """
        instance = self.get_object()
        instance._original_reminder_date = instance.reminder_date
        serializer.save()


class RepaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for repayments.
    """
    queryset = Repayment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request.
        """
        from .serializers import RepaymentSerializer
        return RepaymentSerializer
    
    def perform_update(self, serializer):
        """
        Store the original due date before updating for change detection.
        """
        instance = self.get_object()
        instance._original_due_date = instance.due_date
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def record_payment(self, request, pk=None):
        """
        Record a payment for a repayment.
        """
        repayment = self.get_object()
        amount = request.data.get('amount')
        
        if not amount:
            return Response({
                'status': 'error',
                'message': 'Amount is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Convert to Decimal instead of float to match the model field type
            from decimal import Decimal
            amount = Decimal(str(amount))
        except (ValueError, TypeError):
            return Response({
                'status': 'error',
                'message': 'Amount must be a valid number'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update repayment status based on payment amount
        repayment.paid_amount += amount
        
        if repayment.paid_amount >= repayment.amount:
            repayment.status = 'PAID'
            repayment.paid_date = timezone.now().date()
        elif repayment.paid_amount > 0:
            repayment.status = 'PARTIAL'
        
        repayment.save()
        
        # Create payment record
        payment = Payment.objects.create(
            application=repayment.application,
            amount=amount,
            payment_date=timezone.now().date(),
            payment_method=request.data.get('payment_method', 'BANK_TRANSFER'),
            reference=request.data.get('reference', ''),
            notes=request.data.get('notes', ''),
            created_by=request.user.profile if hasattr(request.user, 'profile') else None
        )
        
        return Response({
            'status': 'success',
            'message': 'Payment recorded successfully',
            'repayment_status': repayment.status,
            'payment_id': payment.id
        })


class ExtensionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for loan extensions.
    """
    queryset = Extension.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request.
        """
        from .serializers import ExtensionSerializer
        return ExtensionSerializer
    
    def perform_create(self, serializer):
        """
        Set created_by when creating an extension.
        """
        created_by = None
        if hasattr(self.request.user, 'profile'):
            created_by = self.request.user.profile
            
        serializer.save(created_by=created_by)
    
    def perform_update(self, serializer):
        """
        Store the original status before updating for change detection.
        """
        instance = self.get_object()
        instance._original_status = instance.status
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve a loan extension.
        """
        extension = self.get_object()
        
        if extension.status != 'PENDING':
            return Response({
                'status': 'error',
                'message': 'Only pending extensions can be approved'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        extension._original_status = extension.status
        extension.status = 'APPROVED'
        extension.approved_by = request.user.profile if hasattr(request.user, 'profile') else None
        extension.save()
        
        # Update the application expiry date
        application = extension.application
        application.expiry_date = extension.new_expiry_date
        application.save()
        
        return Response({
            'status': 'success',
            'message': 'Extension approved successfully'
        })
    
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        """
        Decline a loan extension.
        """
        extension = self.get_object()
        
        if extension.status != 'PENDING':
            return Response({
                'status': 'error',
                'message': 'Only pending extensions can be declined'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        extension._original_status = extension.status
        extension.status = 'DECLINED'
        extension.save()
        
        return Response({
            'status': 'success',
            'message': 'Extension declined successfully'
        })


class FeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for fees.
    """
    queryset = Fee.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request.
        """
        from .serializers import FeeSerializer
        return FeeSerializer
    
    def perform_update(self, serializer):
        """
        Store the original status before updating for change detection.
        """
        instance = self.get_object()
        instance._original_status = instance.status
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        """
        Mark a fee as paid.
        """
        fee = self.get_object()
        
        fee._original_status = fee.status
        fee.status = 'PAID'
        fee.save()
        
        # Create payment record
        payment = Payment.objects.create(
            application=fee.application,
            amount=fee.amount,
            payment_date=timezone.now().date(),
            payment_method=request.data.get('payment_method', 'BANK_TRANSFER'),
            reference=request.data.get('reference', ''),
            notes=f"Payment for {fee.get_fee_type_display()}",
            created_by=request.user.profile if hasattr(request.user, 'profile') else None
        )
        
        return Response({
            'status': 'success',
            'message': 'Fee marked as paid',
            'payment_id': payment.id
        })
    
    @action(detail=True, methods=['post'])
    def waive(self, request, pk=None):
        """
        Waive a fee.
        """
        fee = self.get_object()
        reason = request.data.get('reason', '')
        
        fee._original_status = fee.status
        fee.status = 'WAIVED'
        fee.save()
        
        # Create a note about the waived fee
        Note.objects.create(
            application=fee.application,
            content=f"Fee waived: {fee.get_fee_type_display()} - ${fee.amount}. Reason: {reason}",
            created_by=request.user.profile if hasattr(request.user, 'profile') else None
        )
        
        return Response({
            'status': 'success',
            'message': 'Fee waived successfully'
        })
