from rest_framework import serializers
from .models import BD
from apps.branch.serializers import BranchListSerializer


class BDSerializer(serializers.ModelSerializer):
    """
    Serializer for BD model
    """
    full_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    experience_years = serializers.SerializerMethodField()
    branch_details = BranchListSerializer(source='branch', read_only=True)
    
    class Meta:
        model = BD
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            'branch', 'branch_name', 'branch_details', 'employee_id', 'position',
            'hire_date', 'is_active', 'bio', 'linkedin_profile', 'profile_image',
            'created_at', 'updated_at', 'experience_years'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'full_name', 'branch_name', 'experience_years']
    
    def get_full_name(self, obj):
        """
        Get the full name of the BD
        """
        return obj.get_full_name()
    
    def get_branch_name(self, obj):
        """
        Get the name of the branch this BD belongs to
        """
        return obj.get_branch_name()
    
    def get_experience_years(self, obj):
        """
        Get the number of years of experience based on hire date
        """
        return obj.get_experience_years()


class BDListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing BDs
    """
    full_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    
    class Meta:
        model = BD
        fields = ['id', 'full_name', 'email', 'position', 'branch_name', 'is_active']
    
    def get_full_name(self, obj):
        """
        Get the full name of the BD
        """
        return obj.get_full_name()
    
    def get_branch_name(self, obj):
        """
        Get the name of the branch this BD belongs to
        """
        return obj.get_branch_name()
