from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, Director, Shareholder, FinancialInformation
from .serializers import (
    CompanySerializer, CompanyListSerializer, CompanyDetailSerializer,
    DirectorSerializer, DirectorListSerializer,
    ShareholderSerializer, ShareholderListSerializer,
    FinancialInformationSerializer, FinancialInformationListSerializer
)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for companies
    """
    queryset = Company.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company_type', 'registration_jurisdiction']
    search_fields = ['name', 'trading_name', 'acn', 'abn', 'email', 'industry']
    ordering_fields = ['name', 'registration_date', 'employees_count', 'years_in_business']
    ordering = ['name']
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request
        """
        if self.action == 'list':
            return CompanyListSerializer
        elif self.action == 'retrieve':
            return CompanyDetailSerializer
        return CompanySerializer
    
    @action(detail=True, methods=['get'])
    def directors(self, request, pk=None):
        """
        Return all directors for a company
        """
        company = self.get_object()
        directors = Director.objects.filter(company=company)
        serializer = DirectorListSerializer(directors, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def shareholders(self, request, pk=None):
        """
        Return all shareholders for a company
        """
        company = self.get_object()
        shareholders = Shareholder.objects.filter(company=company)
        serializer = ShareholderListSerializer(shareholders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def financials(self, request, pk=None):
        """
        Return all financial information for a company
        """
        company = self.get_object()
        financials = FinancialInformation.objects.filter(company=company)
        serializer = FinancialInformationListSerializer(financials, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def latest_financial(self, request, pk=None):
        """
        Return the latest financial information for a company
        """
        company = self.get_object()
        financial = company.get_latest_financial_year()
        if financial:
            serializer = FinancialInformationSerializer(financial)
            return Response(serializer.data)
        return Response({"detail": "No financial information available"}, status=status.HTTP_404_NOT_FOUND)


class DirectorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for directors
    """
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'role', 'is_shareholder']
    search_fields = ['first_name', 'last_name', 'email', 'company__name']
    ordering_fields = ['last_name', 'first_name', 'appointment_date']
    ordering = ['last_name', 'first_name']
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request
        """
        if self.action == 'list':
            return DirectorListSerializer
        return DirectorSerializer
    
    @action(detail=False, methods=['get'])
    def by_company(self, request):
        """
        Return directors grouped by company
        """
        companies = Company.objects.all()
        result = []
        
        for company in companies:
            directors = Director.objects.filter(company=company)
            company_data = {
                'id': company.id,
                'name': company.name,
                'directors': DirectorListSerializer(directors, many=True).data
            }
            result.append(company_data)
        
        return Response(result)


class ShareholderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for shareholders
    """
    queryset = Shareholder.objects.all()
    serializer_class = ShareholderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'shareholder_type', 'share_class', 'is_director']
    search_fields = ['individual_first_name', 'individual_last_name', 'corporate_name', 'trust_name', 'company__name']
    ordering_fields = ['shareholding_percentage', 'acquisition_date']
    ordering = ['-shareholding_percentage']
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request
        """
        if self.action == 'list':
            return ShareholderListSerializer
        return ShareholderSerializer
    
    @action(detail=False, methods=['get'])
    def by_company(self, request):
        """
        Return shareholders grouped by company
        """
        companies = Company.objects.all()
        result = []
        
        for company in companies:
            shareholders = Shareholder.objects.filter(company=company)
            company_data = {
                'id': company.id,
                'name': company.name,
                'shareholders': ShareholderListSerializer(shareholders, many=True).data
            }
            result.append(company_data)
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """
        Return shareholders grouped by type
        """
        shareholder_types = dict(Shareholder.SHAREHOLDER_TYPE_CHOICES)
        result = []
        
        for type_code, type_name in shareholder_types.items():
            shareholders = Shareholder.objects.filter(shareholder_type=type_code)
            type_data = {
                'type_code': type_code,
                'type_name': type_name,
                'shareholders': ShareholderListSerializer(shareholders, many=True).data
            }
            result.append(type_data)
        
        return Response(result)


class FinancialInformationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for financial information
    """
    queryset = FinancialInformation.objects.all()
    serializer_class = FinancialInformationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'financial_year', 'source']
    search_fields = ['company__name', 'financial_year']
    ordering_fields = ['financial_year', 'financial_year_end_date', 'annual_revenue', 'annual_profit']
    ordering = ['-financial_year', '-financial_year_end_date']
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request
        """
        if self.action == 'list':
            return FinancialInformationListSerializer
        return FinancialInformationSerializer
    
    @action(detail=False, methods=['get'])
    def by_company(self, request):
        """
        Return financial information grouped by company
        """
        companies = Company.objects.all()
        result = []
        
        for company in companies:
            financials = FinancialInformation.objects.filter(company=company)
            company_data = {
                'id': company.id,
                'name': company.name,
                'financials': FinancialInformationListSerializer(financials, many=True).data
            }
            result.append(company_data)
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def by_year(self, request):
        """
        Return financial information grouped by year
        """
        years = FinancialInformation.objects.values_list('financial_year', flat=True).distinct().order_by('-financial_year')
        result = []
        
        for year in years:
            financials = FinancialInformation.objects.filter(financial_year=year)
            year_data = {
                'year': year,
                'financials': FinancialInformationListSerializer(financials, many=True).data
            }
            result.append(year_data)
        
        return Response(result)
