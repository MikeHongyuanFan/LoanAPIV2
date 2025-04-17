from django.db import models


class Guarantor(models.Model):
    TYPE_CHOICES = (
        ('INDIVIDUAL', 'Individual'),
        ('COMPANY', 'Company'),
    )
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    application = models.ForeignKey('application.Application', on_delete=models.CASCADE, related_name='guarantors')
    guarantor_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Individual guarantor fields
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    id_number = models.CharField(max_length=50, null=True, blank=True)
    id_type = models.CharField(max_length=50, null=True, blank=True)
    
    # Company guarantor fields
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_registration_number = models.CharField(max_length=50, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    
    # Common fields
    relationship_to_borrower = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.guarantor_type == 'INDIVIDUAL':
            return f"{self.name} - Individual Guarantor"
        else:
            return f"{self.company_name} - Company Guarantor"
