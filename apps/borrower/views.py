from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
import json

from .models import Borrower, BorrowerMergeRecord
from .serializers import BorrowerSerializer, BorrowerMergeRecordSerializer, BorrowerMergeSerializer


class BorrowerListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating borrowers.
    """
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'email', 'phone', 'id_number']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Check if potential duplicates were found
        response_data = serializer.data
        if 'potential_duplicates' in serializer.context:
            response_data = {
                'borrower': serializer.data,
                'potential_duplicates': serializer.context['potential_duplicates'],
                'warning': 'Potential duplicate borrowers found. Please review before proceeding.'
            }
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class BorrowerDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating a borrower.
    """
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer
    permission_classes = [IsAuthenticated]


class BorrowerSearchView(generics.ListAPIView):
    """
    API endpoint for searching borrowers.
    """
    serializer_class = BorrowerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email', 'phone', 'id_number']
    
    def get_queryset(self):
        return Borrower.objects.all()


class BorrowerApplicationsView(generics.ListAPIView):
    """
    API endpoint for listing applications linked to a borrower.
    """
    serializer_class = None  # Will be imported from application app
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        borrower_id = self.kwargs['pk']
        return self.serializer_class.Meta.model.objects.filter(borrower_id=borrower_id)


class BorrowerDuplicateCheckView(APIView):
    """
    API endpoint for checking potential duplicate borrowers.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Create a temporary borrower object from the request data
        borrower_data = request.data
        temp_borrower = Borrower(
            name=borrower_data.get('name', ''),
            email=borrower_data.get('email', ''),
            phone=borrower_data.get('phone', ''),
            id_number=borrower_data.get('id_number', ''),
            date_of_birth=borrower_data.get('date_of_birth'),
            gender=borrower_data.get('gender', ''),
            address=borrower_data.get('address', ''),
            id_type=borrower_data.get('id_type', ''),
            employment_status=borrower_data.get('employment_status', ''),
            employer=borrower_data.get('employer', ''),
            income=borrower_data.get('income', 0)
        )
        
        # Find potential duplicates
        potential_duplicates = Borrower.find_potential_duplicates(temp_borrower)
        
        if not potential_duplicates.exists():
            return Response({
                'has_duplicates': False,
                'message': 'No potential duplicates found.'
            })
        
        # Format duplicate information
        duplicate_info = []
        for dup in potential_duplicates:
            match_reasons = []
            if dup.name.lower() == temp_borrower.name.lower():
                match_reasons.append('name')
            if dup.email.lower() == temp_borrower.email.lower():
                match_reasons.append('email')
            if dup.phone == temp_borrower.phone:
                match_reasons.append('phone')
            if dup.id_number == temp_borrower.id_number:
                match_reasons.append('ID number')
            
            duplicate_info.append({
                'id': dup.id,
                'name': dup.name,
                'email': dup.email,
                'phone': dup.phone,
                'date_of_birth': dup.date_of_birth,
                'match_reasons': match_reasons
            })
        
        return Response({
            'has_duplicates': True,
            'potential_duplicates': duplicate_info,
            'message': 'Potential duplicate borrowers found.'
        })


class BorrowerMergeView(APIView):
    """
    API endpoint for merging duplicate borrowers.
    """
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = BorrowerMergeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        primary_borrower = serializer.primary_borrower
        duplicate_borrower = serializer.duplicate_borrower
        
        # Store duplicate borrower data before merging
        duplicate_data = {
            'id': duplicate_borrower.id,
            'name': duplicate_borrower.name,
            'email': duplicate_borrower.email,
            'phone': duplicate_borrower.phone,
            'address': duplicate_borrower.address,
            'date_of_birth': str(duplicate_borrower.date_of_birth),
            'gender': duplicate_borrower.gender,
            'id_number': duplicate_borrower.id_number,
            'id_type': duplicate_borrower.id_type,
            'employment_status': duplicate_borrower.employment_status,
            'employer': duplicate_borrower.employer,
            'income': str(duplicate_borrower.income),
            'created_at': str(duplicate_borrower.created_at),
            'updated_at': str(duplicate_borrower.updated_at)
        }
        
        # Create merge record
        merge_record = BorrowerMergeRecord.objects.create(
            primary_borrower=primary_borrower,
            merged_borrower=duplicate_borrower,
            merged_borrower_data=duplicate_data,
            merged_by=request.user.profile if hasattr(request.user, 'profile') else None
        )
        
        # Update all related applications to point to the primary borrower
        if hasattr(duplicate_borrower, 'applications'):
            duplicate_borrower.applications.update(borrower=primary_borrower)
        
        # Update all related guarantors to point to the primary borrower
        if hasattr(duplicate_borrower, 'guarantors'):
            duplicate_borrower.guarantors.update(borrower=primary_borrower)
        
        # Return the merge record
        return Response({
            'message': 'Borrowers successfully merged',
            'merge_record': BorrowerMergeRecordSerializer(merge_record).data
        })


class BorrowerMergeHistoryView(generics.ListAPIView):
    """
    API endpoint for listing borrower merge history.
    """
    queryset = BorrowerMergeRecord.objects.all()
    serializer_class = BorrowerMergeRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['primary_borrower', 'merged_by']
