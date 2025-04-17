from .models import AuditLog
import json


class AuditLogMiddleware:
    """
    Middleware to log user actions for auditing purposes.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        
        # Skip logging for certain paths
        if self._should_skip_logging(request.path):
            return response
        
        # Log the action
        self._log_action(request, response)
        
        return response
    
    def _should_skip_logging(self, path):
        """
        Determine if logging should be skipped for this path.
        """
        skip_paths = [
            '/static/',
            '/media/',
            '/admin/jsi18n/',
            '/favicon.ico',
        ]
        
        return any(path.startswith(skip_path) for skip_path in skip_paths)
    
    def _log_action(self, request, response):
        """
        Log the action to the audit log.
        """
        # Only log if user is authenticated
        if not request.user.is_authenticated:
            return
        
        # Determine action type
        action = self._determine_action(request.method)
        
        # Determine entity type and ID
        entity_type, entity_id = self._determine_entity(request.path)
        
        # Create audit log entry
        AuditLog.objects.create(
            user=request.user,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=self._create_description(request, action, entity_type),
            ip_address=self._get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    
    def _determine_action(self, method):
        """
        Determine the action based on the HTTP method.
        """
        action_map = {
            'GET': 'READ',
            'POST': 'CREATE',
            'PUT': 'UPDATE',
            'PATCH': 'UPDATE',
            'DELETE': 'DELETE'
        }
        
        return action_map.get(method, 'OTHER')
    
    def _determine_entity(self, path):
        """
        Determine the entity type and ID from the path.
        """
        # Extract entity type and ID from path
        # This is a simplified implementation
        parts = path.strip('/').split('/')
        
        if len(parts) < 2:
            return 'Unknown', None
        
        # Handle API paths
        if parts[0] == 'api':
            parts = parts[1:]
        
        entity_type = parts[0]
        entity_id = parts[1] if len(parts) > 1 and parts[1].isdigit() else None
        
        return entity_type, entity_id
    
    def _create_description(self, request, action, entity_type):
        """
        Create a description for the audit log entry.
        """
        method = request.method
        path = request.path
        
        description = f"{method} request to {path}"
        
        # Add request body for non-GET requests, excluding sensitive data
        if method != 'GET' and hasattr(request, 'body') and request.body:
            try:
                body = json.loads(request.body)
                # Remove sensitive fields
                sensitive_fields = ['password', 'token', 'secret', 'credit_card']
                for field in sensitive_fields:
                    if field in body:
                        body[field] = '***REDACTED***'
                
                description += f" with data: {json.dumps(body)}"
            except json.JSONDecodeError:
                pass
        
        return description
    
    def _get_client_ip(self, request):
        """
        Get the client IP address from the request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
