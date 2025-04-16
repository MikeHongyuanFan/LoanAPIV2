from django.utils import timezone
from .models import AuditLog, UserProfile


class AuditLogMiddleware:
    """
    Middleware to log user actions for auditing purposes.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        
        # Only log authenticated requests
        if request.user.is_authenticated:
            self.log_action(request, response)
        
        return response
    
    def log_action(self, request, response):
        """
        Log the user action based on the request method and path.
        """
        # Skip logging for static files, admin media, etc.
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return
        
        # Determine action based on HTTP method
        method_to_action = {
            'GET': 'READ',
            'POST': 'CREATE',
            'PUT': 'UPDATE',
            'PATCH': 'UPDATE',
            'DELETE': 'DELETE',
        }
        
        action = method_to_action.get(request.method, 'READ')
        
        # Special cases for login/logout
        if request.path.endswith('/login/') and request.method == 'POST':
            action = 'LOGIN'
            # Update last login IP
            try:
                profile = UserProfile.objects.get(user=request.user)
                profile.last_login_ip = self.get_client_ip(request)
                profile.save(update_fields=['last_login_ip'])
            except UserProfile.DoesNotExist:
                pass
        elif request.path.endswith('/logout/') and request.method == 'POST':
            action = 'LOGOUT'
        
        # Determine resource type from path
        resource_type = self.get_resource_type(request.path)
        
        # Determine resource ID if available
        resource_id = self.get_resource_id(request.path)
        
        # Create audit log entry
        try:
            AuditLog.objects.create(
                user=request.user.profile if hasattr(request.user, 'profile') else None,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=self.get_request_details(request),
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                timestamp=timezone.now()
            )
        except Exception as e:
            # Log the error but don't interrupt the request
            print(f"Error creating audit log: {e}")
    
    def get_resource_type(self, path):
        """
        Extract resource type from the request path.
        """
        path_parts = path.strip('/').split('/')
        
        # Map path prefixes to resource types
        resource_mapping = {
            'applications': 'APPLICATION',
            'borrowers': 'BORROWER',
            'guarantors': 'GUARANTOR',
            'brokers': 'BROKER',
            'valuers': 'VALUER',
            'qs': 'QS',
            'products': 'PRODUCT',
            'documents': 'DOCUMENT',
            'notifications': 'NOTIFICATION',
            'users': 'USER',
            'reports': 'REPORT',
        }
        
        if path_parts and path_parts[0] in resource_mapping:
            return resource_mapping[path_parts[0]]
        
        return 'OTHER'
    
    def get_resource_id(self, path):
        """
        Extract resource ID from the request path if available.
        """
        path_parts = path.strip('/').split('/')
        
        # Check if there's an ID in the path (typically the second part)
        if len(path_parts) > 1 and path_parts[1].isdigit():
            return path_parts[1]
        
        return None
    
    def get_request_details(self, request):
        """
        Extract relevant details from the request.
        """
        details = {
            'method': request.method,
            'path': request.path,
        }
        
        # Add query parameters for GET requests
        if request.method == 'GET' and request.GET:
            details['query_params'] = dict(request.GET)
        
        # Add request body for POST/PUT/PATCH requests (excluding sensitive data)
        if request.method in ['POST', 'PUT', 'PATCH'] and hasattr(request, 'data'):
            # Create a copy of the data to avoid modifying the original
            data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
            
            # Remove sensitive fields
            sensitive_fields = ['password', 'token', 'secret', 'credit_card', 'ssn']
            for field in sensitive_fields:
                if field in data:
                    data[field] = '***REDACTED***'
            
            details['request_data'] = data
        
        return str(details)
    
    def get_client_ip(self, request):
        """
        Extract client IP address from request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
