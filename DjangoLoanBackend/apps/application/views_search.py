from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Application
from .serializers import ApplicationSerializer
from apps.authentication.permissions import IsStaff


class AdvancedSearchView(APIView):
    """
    API endpoint for advanced search across applications and related entities.
    """
    permission_classes = [IsAuthenticated, IsStaff]
    
    def get(self, request):
        # Get search parameters
        query = request.query_params.get('q', '')
        search_type = request.query_params.get('type', 'basic')  # basic, full_text, or combined
        
        if not query:
            return Response({
                'results': [],
                'count': 0,
                'message': 'No search query provided'
            })
        
        # Basic search (exact matches and simple contains)
        if search_type == 'basic' or search_type == 'combined':
            basic_results = self._perform_basic_search(query)
        else:
            basic_results = []
        
        # Full-text search (if PostgreSQL is configured)
        if search_type == 'full_text' or search_type == 'combined':
            try:
                full_text_results = self._perform_full_text_search(query)
            except Exception as e:
                full_text_results = []
                # If PostgreSQL full-text search is not available, fall back to basic search
                if search_type == 'full_text' and not basic_results:
                    basic_results = self._perform_basic_search(query)
        else:
            full_text_results = []
        
        # Combine and deduplicate results
        combined_ids = set()
        combined_results = []
        
        # Add basic search results
        for result in basic_results:
            if result['id'] not in combined_ids:
                combined_ids.add(result['id'])
                combined_results.append(result)
        
        # Add full-text search results
        for result in full_text_results:
            if result['id'] not in combined_ids:
                combined_ids.add(result['id'])
                combined_results.append(result)
        
        return Response({
            'results': combined_results,
            'count': len(combined_results),
            'search_query': query,
            'search_type': search_type
        })
    
    def _perform_basic_search(self, query):
        """
        Perform basic search using Q objects and contains/exact lookups.
        """
        # Search in Application model
        application_results = Application.objects.filter(
            Q(reference_number__icontains=query) |
            Q(status__iexact=query) |
            Q(stage__iexact=query) |
            Q(loan_type__iexact=query) |
            Q(borrower__name__icontains=query) |
            Q(borrower__email__icontains=query) |
            Q(borrower__phone__icontains=query) |
            Q(broker__name__icontains=query) |
            Q(broker__email__icontains=query) |
            Q(broker__company__icontains=query) |
            Q(property_address__icontains=query)
        ).distinct()
        
        # Format results
        results = []
        for app in application_results:
            results.append({
                'id': app.id,
                'reference_number': app.reference_number,
                'type': 'application',
                'status': app.status,
                'stage': app.stage,
                'loan_amount': app.loan_amount,
                'borrower_name': app.borrower.name if app.borrower else None,
                'broker_name': app.broker.name if app.broker else None,
                'property_address': app.property_address,
                'created_at': app.created_at,
                'match_field': self._determine_match_field(app, query)
            })
        
        return results
    
    def _perform_full_text_search(self, query):
        """
        Perform full-text search using PostgreSQL's full-text search capabilities.
        """
        # Create search vector for multiple fields
        search_vector = SearchVector(
            'reference_number', 'status', 'stage', 'loan_type', 'property_address',
            'borrower__name', 'borrower__email', 'broker__name', 'broker__company'
        )
        
        # Create search query
        search_query = SearchQuery(query)
        
        # Search with ranking
        application_results = Application.objects.annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gt=0).order_by('-rank')
        
        # Format results
        results = []
        for app in application_results:
            results.append({
                'id': app.id,
                'reference_number': app.reference_number,
                'type': 'application',
                'status': app.status,
                'stage': app.stage,
                'loan_amount': app.loan_amount,
                'borrower_name': app.borrower.name if app.borrower else None,
                'broker_name': app.broker.name if app.broker else None,
                'property_address': app.property_address,
                'created_at': app.created_at,
                'rank': app.rank,
                'match_field': self._determine_match_field(app, query)
            })
        
        return results
    
    def _determine_match_field(self, application, query):
        """
        Determine which field matched the search query.
        """
        query = query.lower()
        
        if query in application.reference_number.lower():
            return 'reference_number'
        elif application.status and query in application.status.lower():
            return 'status'
        elif application.stage and query in application.stage.lower():
            return 'stage'
        elif application.loan_type and query in application.loan_type.lower():
            return 'loan_type'
        elif application.property_address and query in application.property_address.lower():
            return 'property_address'
        elif application.borrower and application.borrower.name and query in application.borrower.name.lower():
            return 'borrower_name'
        elif application.borrower and application.borrower.email and query in application.borrower.email.lower():
            return 'borrower_email'
        elif application.broker and application.broker.name and query in application.broker.name.lower():
            return 'broker_name'
        elif application.broker and application.broker.company and query in application.broker.company.lower():
            return 'broker_company'
        
        return 'unknown'


class GlobalSearchView(APIView):
    """
    API endpoint for searching across all entities in the system.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get search parameters
        query = request.query_params.get('q', '')
        
        if not query:
            return Response({
                'results': {
                    'applications': [],
                    'borrowers': [],
                    'brokers': [],
                    'guarantors': [],
                    'documents': []
                },
                'count': 0,
                'message': 'No search query provided'
            })
        
        # Search in Application model
        application_results = Application.objects.filter(
            Q(reference_number__icontains=query) |
            Q(status__iexact=query) |
            Q(stage__iexact=query) |
            Q(property_address__icontains=query)
        ).distinct()[:10]  # Limit to 10 results
        
        # Format application results
        applications = []
        for app in application_results:
            applications.append({
                'id': app.id,
                'reference_number': app.reference_number,
                'status': app.status,
                'stage': app.stage,
                'loan_amount': app.loan_amount,
                'borrower_name': app.borrower.name if app.borrower else None,
                'property_address': app.property_address,
                'created_at': app.created_at
            })
        
        # Search in Borrower model (would be imported from apps.borrower.models)
        # This is a placeholder - in a real implementation, you would import and use the actual Borrower model
        borrowers = []
        
        # Search in Broker model (would be imported from apps.broker.models)
        # This is a placeholder - in a real implementation, you would import and use the actual Broker model
        brokers = []
        
        # Search in Guarantor model (would be imported from apps.guarantor.models)
        # This is a placeholder - in a real implementation, you would import and use the actual Guarantor model
        guarantors = []
        
        # Search in Document model (would be imported from apps.document.models)
        # This is a placeholder - in a real implementation, you would import and use the actual Document model
        documents = []
        
        # Count total results
        total_count = len(applications) + len(borrowers) + len(brokers) + len(guarantors) + len(documents)
        
        return Response({
            'results': {
                'applications': applications,
                'borrowers': borrowers,
                'brokers': brokers,
                'guarantors': guarantors,
                'documents': documents
            },
            'count': total_count,
            'search_query': query
        })
