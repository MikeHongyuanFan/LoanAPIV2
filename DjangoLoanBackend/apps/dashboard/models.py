from django.db import models


class DashboardWidget(models.Model):
    """
    Model to store dashboard widget configurations.
    """
    TYPE_CHOICES = (
        ('CHART', 'Chart'),
        ('TABLE', 'Table'),
        ('METRIC', 'Metric'),
        ('LIST', 'List'),
    )
    
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    configuration = models.JSONField(default=dict)  # Store widget configuration
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class UserDashboardPreference(models.Model):
    """
    Model to store user dashboard preferences.
    """
    user_profile = models.ForeignKey('authentication.UserProfile', on_delete=models.CASCADE, 
                                    related_name='dashboard_preferences')
    widgets = models.ManyToManyField(DashboardWidget, through='UserWidgetConfiguration')
    layout = models.JSONField(default=dict)  # Store layout configuration
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dashboard preferences for {self.user_profile}"


class UserWidgetConfiguration(models.Model):
    """
    Model to store user-specific widget configurations.
    """
    dashboard_preference = models.ForeignKey(UserDashboardPreference, on_delete=models.CASCADE)
    widget = models.ForeignKey(DashboardWidget, on_delete=models.CASCADE)
    position = models.IntegerField()
    configuration = models.JSONField(default=dict)  # Store user-specific configuration
    
    class Meta:
        ordering = ['position']
    
    def __str__(self):
        return f"{self.widget.name} for {self.dashboard_preference.user_profile}"
