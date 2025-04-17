from rest_framework import serializers
from .models import Company, Director, Shareholder, FinancialInformation


class CompanyAddressSerializer(serializers.Serializer):
    """
    Serializer for structured address data
    """
    line1 = serializers.CharField()
    line2 = serializers.CharField(allow_null=True, required=False)
    city = serializers.CharField()
    state = serializers.CharField()
    postal_code = serializers.CharField()
    country = serializers.CharField()


class DirectorListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing directors
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Director
        fields = ['id', 'full_name', 'role', 'appointment_date', 'phone', 'email']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class ShareholderListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing shareholders
    """
    shareholder_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Shareholder
        fields = ['id', 'shareholder_name', 'shareholder_type', 'shareholding_percentage', 'share_class', 'is_director']
    
    def get_shareholder_name(self, obj):
        return obj.get_shareholder_name()


class FinancialInformationListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing financial information
    """
    current_ratio = serializers.SerializerMethodField()
    debt_to_equity_ratio = serializers.SerializerMethodField()
    profit_margin = serializers.SerializerMethodField()
    
    class Meta:
        model = FinancialInformation
        fields = [
            'id', 'financial_year', 'annual_revenue', 'annual_profit', 
            'current_ratio', 'debt_to_equity_ratio', 'profit_margin', 'source'
        ]
    
    def get_current_ratio(self, obj):
        return obj.get_current_ratio()
    
    def get_debt_to_equity_ratio(self, obj):
        return obj.get_debt_to_equity_ratio()
    
    def get_profit_margin(self, obj):
        return obj.get_profit_margin()


class CompanyListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing companies
    """
    directors_count = serializers.SerializerMethodField()
    shareholders_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'trading_name', 'company_type', 'acn', 'abn',
            'registration_date', 'phone', 'email', 'industry',
            'directors_count', 'shareholders_count'
        ]
    
    def get_directors_count(self, obj):
        return obj.get_directors_count()
    
    def get_shareholders_count(self, obj):
        return obj.get_shareholders_count()


class DirectorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Director model
    """
    full_name = serializers.SerializerMethodField(read_only=True)
    residential_address = serializers.SerializerMethodField(read_only=True)
    is_shareholder = serializers.SerializerMethodField(read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = Director
        fields = [
            'id', 'company', 'company_name', 'first_name', 'middle_name', 'last_name',
            'full_name', 'date_of_birth', 'director_id', 'appointment_date', 'role',
            'residential_address_line1', 'residential_address_line2', 'residential_city',
            'residential_state', 'residential_postal_code', 'residential_country',
            'residential_address', 'phone', 'email', 'identification_type',
            'identification_number', 'identification_expiry', 'is_shareholder',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_residential_address(self, obj):
        return obj.get_residential_address()
    
    def get_is_shareholder(self, obj):
        return obj.is_shareholder()


class ShareholderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Shareholder model
    """
    shareholder_name = serializers.SerializerMethodField(read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    director_name = serializers.CharField(source='director.get_full_name', read_only=True)
    
    class Meta:
        model = Shareholder
        fields = [
            'id', 'company', 'company_name', 'shareholder_type', 'shareholder_name',
            'individual_first_name', 'individual_last_name', 'individual_date_of_birth',
            'corporate_name', 'corporate_acn', 'corporate_abn',
            'trust_name', 'trust_abn', 'trust_type',
            'shareholding_percentage', 'share_class', 'acquisition_date',
            'is_director', 'director', 'director_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_shareholder_name(self, obj):
        return obj.get_shareholder_name()
    
    def validate(self, data):
        """
        Validate the shareholder data based on shareholder_type
        """
        shareholder_type = data.get('shareholder_type')
        
        if shareholder_type == 'INDIVIDUAL':
            if not data.get('individual_first_name') or not data.get('individual_last_name') or not data.get('individual_date_of_birth'):
                raise serializers.ValidationError("Individual shareholder must have first name, last name, and date of birth")
        elif shareholder_type == 'CORPORATE':
            if not data.get('corporate_name'):
                raise serializers.ValidationError("Corporate shareholder must have a company name")
        elif shareholder_type == 'TRUST':
            if not data.get('trust_name'):
                raise serializers.ValidationError("Trust shareholder must have a trust name")
        
        is_director = data.get('is_director')
        director = data.get('director')
        
        if is_director and not director:
            raise serializers.ValidationError("If shareholder is a director, director field must be set")
        
        if director and shareholder_type != 'INDIVIDUAL':
            raise serializers.ValidationError("Only individual shareholders can be directors")
        
        return data


class FinancialInformationSerializer(serializers.ModelSerializer):
    """
    Serializer for the FinancialInformation model
    """
    current_ratio = serializers.SerializerMethodField(read_only=True)
    debt_to_equity_ratio = serializers.SerializerMethodField(read_only=True)
    profit_margin = serializers.SerializerMethodField(read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = FinancialInformation
        fields = [
            'id', 'company', 'company_name', 'financial_year', 'financial_year_end_date',
            'annual_revenue', 'annual_profit', 'total_assets', 'total_liabilities',
            'current_assets', 'current_liabilities', 'equity', 'ebitda',
            'current_ratio', 'debt_to_equity_ratio', 'profit_margin',
            'source', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_current_ratio(self, obj):
        return obj.get_current_ratio()
    
    def get_debt_to_equity_ratio(self, obj):
        return obj.get_debt_to_equity_ratio()
    
    def get_profit_margin(self, obj):
        return obj.get_profit_margin()


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for the Company model
    """
    registered_address = serializers.SerializerMethodField(read_only=True)
    business_address = serializers.SerializerMethodField(read_only=True)
    directors = DirectorListSerializer(many=True, read_only=True)
    shareholders = ShareholderListSerializer(many=True, read_only=True)
    latest_financial = serializers.SerializerMethodField(read_only=True)
    directors_count = serializers.SerializerMethodField(read_only=True)
    shareholders_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'trading_name', 'company_type',
            'acn', 'abn', 'registration_date', 'registration_jurisdiction',
            'registered_address_line1', 'registered_address_line2', 'registered_city',
            'registered_state', 'registered_postal_code', 'registered_country',
            'registered_address',
            'business_address_line1', 'business_address_line2', 'business_city',
            'business_state', 'business_postal_code', 'business_country',
            'business_address',
            'phone', 'email', 'website',
            'industry', 'business_description', 'employees_count', 'years_in_business',
            'directors', 'shareholders', 'latest_financial',
            'directors_count', 'shareholders_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_registered_address(self, obj):
        return obj.get_registered_address()
    
    def get_business_address(self, obj):
        return obj.get_business_address()
    
    def get_latest_financial(self, obj):
        latest = obj.get_latest_financial_year()
        if latest:
            return FinancialInformationListSerializer(latest).data
        return None
    
    def get_directors_count(self, obj):
        return obj.get_directors_count()
    
    def get_shareholders_count(self, obj):
        return obj.get_shareholders_count()


class CompanyDetailSerializer(CompanySerializer):
    """
    Detailed serializer for the Company model including all related data
    """
    financials = FinancialInformationListSerializer(many=True, read_only=True)
    
    class Meta(CompanySerializer.Meta):
        fields = CompanySerializer.Meta.fields + ['financials']
