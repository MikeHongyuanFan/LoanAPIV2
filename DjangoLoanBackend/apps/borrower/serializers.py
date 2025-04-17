from rest_framework import serializers
from .models import Borrower, BorrowerMergeRecord


class BorrowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Borrower model.
    """
    class Meta:
        model = Borrower
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        """
        Check for potential duplicates when creating a new borrower.
        """
        # Only check for duplicates on create, not update
        if self.instance is None:
            borrower = Borrower(**data)
            potential_duplicates = Borrower.find_potential_duplicates(borrower)
            
            if potential_duplicates.exists():
                duplicate_info = []
                for dup in potential_duplicates:
                    match_reasons = []
                    if dup.name.lower() == data['name'].lower():
                        match_reasons.append('name')
                    if dup.email.lower() == data['email'].lower():
                        match_reasons.append('email')
                    if dup.phone == data['phone']:
                        match_reasons.append('phone')
                    if dup.id_number == data['id_number']:
                        match_reasons.append('ID number')
                    
                    duplicate_info.append({
                        'id': dup.id,
                        'name': dup.name,
                        'email': dup.email,
                        'phone': dup.phone,
                        'match_reasons': match_reasons
                    })
                
                # Add warning about potential duplicates
                self.context['potential_duplicates'] = duplicate_info
        
        return data


class BorrowerMergeRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the BorrowerMergeRecord model.
    """
    primary_borrower_name = serializers.CharField(source='primary_borrower.name', read_only=True)
    merged_borrower_name = serializers.CharField(source='merged_borrower.name', read_only=True)
    merged_by_name = serializers.CharField(source='merged_by.user.username', read_only=True)
    
    class Meta:
        model = BorrowerMergeRecord
        fields = [
            'id', 'primary_borrower', 'primary_borrower_name',
            'merged_borrower', 'merged_borrower_name',
            'merged_borrower_data', 'merged_at',
            'merged_by', 'merged_by_name'
        ]
        read_only_fields = ['merged_at']


class BorrowerMergeSerializer(serializers.Serializer):
    """
    Serializer for merging two borrowers.
    """
    primary_borrower_id = serializers.IntegerField()
    duplicate_borrower_id = serializers.IntegerField()
    
    def validate(self, data):
        """
        Validate that both borrowers exist and are different.
        """
        primary_id = data['primary_borrower_id']
        duplicate_id = data['duplicate_borrower_id']
        
        if primary_id == duplicate_id:
            raise serializers.ValidationError("Cannot merge a borrower with itself")
        
        try:
            self.primary_borrower = Borrower.objects.get(pk=primary_id)
        except Borrower.DoesNotExist:
            raise serializers.ValidationError("Primary borrower does not exist")
        
        try:
            self.duplicate_borrower = Borrower.objects.get(pk=duplicate_id)
        except Borrower.DoesNotExist:
            raise serializers.ValidationError("Duplicate borrower does not exist")
        
        return data
