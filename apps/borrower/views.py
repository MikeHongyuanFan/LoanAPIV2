from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q
from .models import Borrower, BorrowerMergeRecord

class BorrowerListCreateView(generics.ListCreateAPIView):
    """
    List all borrowers or create a new borrower
    """
    queryset = Borrower.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - in a real implementation, you would have a proper serializer
        from rest_framework import serializers
        
        class BorrowerSerializer(serializers.ModelSerializer):
            class Meta:
                model = Borrower
                fields = '__all__'
                
        return BorrowerSerializer

class BorrowerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a borrower
    """
    queryset = Borrower.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - in a real implementation, you would have a proper serializer
        from rest_framework import serializers
        
        class BorrowerSerializer(serializers.ModelSerializer):
            class Meta:
                model = Borrower
                fields = '__all__'
                
        return BorrowerSerializer

class BorrowerSearchView(generics.ListAPIView):
    """
    Search for borrowers
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - in a real implementation, you would have a proper serializer
        from rest_framework import serializers
        
        class BorrowerSerializer(serializers.ModelSerializer):
            class Meta:
                model = Borrower
                fields = '__all__'
                
        return BorrowerSerializer
    
    def get_queryset(self):
        """
        Filter borrowers based on query parameters
        """
        queryset = Borrower.objects.all()
        
        # Filter by name
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        # Filter by email
        email = self.request.query_params.get('email', None)
        if email:
            queryset = queryset.filter(email__icontains=email)
        
        # Filter by phone
        phone = self.request.query_params.get('phone', None)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
            
        return queryset

class BorrowerMergeView(views.APIView):
    """
    Merge two borrower records
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Get the primary and duplicate borrower IDs
        primary_borrower_id = request.data.get('primary_borrower_id')
        duplicate_borrower_id = request.data.get('duplicate_borrower_id')
        fields_to_keep = request.data.get('fields_to_keep', {})
        
        if not primary_borrower_id or not duplicate_borrower_id:
            return Response({
                'error': 'Both primary_borrower_id and duplicate_borrower_id are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            primary = Borrower.objects.get(id=primary_borrower_id)
            duplicate = Borrower.objects.get(id=duplicate_borrower_id)
        except Borrower.DoesNotExist:
            return Response({
                'error': 'One or both borrowers do not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Perform the merge in a transaction
        with transaction.atomic():
            # Store the duplicate borrower data before any changes
            duplicate_data = {
                'id': duplicate.id,
                'name': duplicate.name,
                'email': duplicate.email,
                'phone': duplicate.phone,
                'address': duplicate.address,
                'date_of_birth': str(duplicate.date_of_birth),
                'gender': duplicate.gender,
                'id_number': duplicate.id_number,
                'id_type': duplicate.id_type,
                'employment_status': duplicate.employment_status,
                'employer': duplicate.employer,
                'income': str(duplicate.income)
            }
            
            # Update primary borrower with fields from duplicate if specified
            for field, source in fields_to_keep.items():
                if source == 'duplicate' and hasattr(primary, field) and hasattr(duplicate, field):
                    setattr(primary, field, getattr(duplicate, field))
            
            primary.save()
            
            # Create a merge record
            merge_record = BorrowerMergeRecord.objects.create(
                primary_borrower=primary,
                merged_borrower_data=duplicate_data,
                merged_by=request.user.profile if hasattr(request.user, 'profile') else None
            )
            
            # Update applications to point to the primary borrower
            if hasattr(duplicate, 'application_set'):
                duplicate.application_set.update(borrower=primary)
            
            # Delete the duplicate borrower
            duplicate.delete()
        
        return Response({
            'message': 'Borrowers merged successfully',
            'merge_record_id': merge_record.id
        }, status=status.HTTP_200_OK)


class BorrowerCheckDuplicatesView(views.APIView):
    """
    Check for potential duplicate borrowers.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Extract search criteria
        name = request.data.get('name')
        email = request.data.get('email')
        date_of_birth = request.data.get('date_of_birth')
        phone = request.data.get('phone')
        id_number = request.data.get('id_number')
        
        # Build query
        query = Q()
        if name:
            query |= Q(name__iexact=name)
        if email:
            query |= Q(email__iexact=email)
        if date_of_birth:
            query |= Q(date_of_birth=date_of_birth)
        if phone:
            query |= Q(phone=phone)
        if id_number:
            query |= Q(id_number__iexact=id_number)
        
        # Find potential duplicates
        duplicates = Borrower.objects.filter(query)
        
        # Serialize and return results
        serializer = self.get_serializer_class()(duplicates, many=True)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        # Placeholder - in a real implementation, you would have a proper serializer
        from rest_framework import serializers
        
        class BorrowerSerializer(serializers.ModelSerializer):
            class Meta:
                model = Borrower
                fields = '__all__'
                
        return BorrowerSerializer


class BorrowerMergeHistoryView(generics.ListAPIView):
    """
    List borrower merge history records.
    """
    permission_classes = [IsAuthenticated]
    queryset = BorrowerMergeRecord.objects.all().order_by('-merged_at')
    
    def get_serializer_class(self):
        from rest_framework import serializers
        
        class BorrowerMergeRecordSerializer(serializers.ModelSerializer):
            primary_borrower_id = serializers.IntegerField(source='primary_borrower.id')
            primary_borrower_name = serializers.CharField(source='primary_borrower.name')
            merged_by_name = serializers.CharField(source='merged_by.username', default=None)
            
            class Meta:
                model = BorrowerMergeRecord
                fields = ['id', 'primary_borrower_id', 'primary_borrower_name', 
                          'merged_borrower_data', 'merged_at', 'merged_by', 'merged_by_name']
                
        return BorrowerMergeRecordSerializer
