from django.db import models
from django.db.models import Q
from django.utils import timezone


class Borrower(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    EMPLOYMENT_STATUS_CHOICES = (
        ('EMPLOYED', 'Employed'),
        ('SELF_EMPLOYED', 'Self-Employed'),
        ('UNEMPLOYED', 'Unemployed'),
        ('RETIRED', 'Retired'),
    )
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    id_number = models.CharField(max_length=50)
    id_type = models.CharField(max_length=50)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES)
    employer = models.CharField(max_length=255, null=True, blank=True)
    income = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def find_potential_duplicates(cls, borrower):
        """
        Find potential duplicate borrowers based on name, email, phone, or ID.
        """
        if isinstance(borrower, cls):
            # If borrower is already a model instance
            query = Q(name__iexact=borrower.name) | \
                    Q(email__iexact=borrower.email) | \
                    Q(phone=borrower.phone) | \
                    Q(id_number=borrower.id_number)
            
            # Exclude the borrower itself if it has an ID
            if borrower.id:
                return cls.objects.filter(query).exclude(id=borrower.id)
            return cls.objects.filter(query)
        else:
            # If borrower is a dictionary or other data structure
            query = Q()
            if 'name' in borrower:
                query |= Q(name__iexact=borrower['name'])
            if 'email' in borrower:
                query |= Q(email__iexact=borrower['email'])
            if 'phone' in borrower:
                query |= Q(phone=borrower['phone'])
            if 'id_number' in borrower:
                query |= Q(id_number=borrower['id_number'])
            
            return cls.objects.filter(query)


class BorrowerMergeRecord(models.Model):
    primary_borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='primary_merge_records')
    merged_borrower_data = models.JSONField()  # Store the data of the merged borrower
    merged_at = models.DateTimeField(default=timezone.now)
    merged_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Merge into {self.primary_borrower.name} on {self.merged_at}"
