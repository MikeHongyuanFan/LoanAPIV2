from django.db import models
from django.utils import timezone
from django.db.models import Q


class Borrower(models.Model):
    """
    Model representing a borrower who applies for loans.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    id_number = models.CharField(max_length=50, unique=True)
    id_type = models.CharField(max_length=50)
    employment_status = models.CharField(max_length=50)
    employer = models.CharField(max_length=255, blank=True, null=True)
    income = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def find_potential_duplicates(cls, borrower):
        """
        Find potential duplicate borrowers based on name, email, phone, or ID number.
        
        Args:
            borrower: A Borrower instance to check for duplicates
            
        Returns:
            QuerySet of potential duplicate Borrower instances
        """
        if isinstance(borrower, cls):
            # Exclude the current borrower if it's already saved
            exclude_id = Q()
            if borrower.id:
                exclude_id = ~Q(id=borrower.id)
                
            return cls.objects.filter(
                (
                    Q(name__iexact=borrower.name) |
                    Q(email__iexact=borrower.email) |
                    Q(phone=borrower.phone) |
                    Q(id_number=borrower.id_number)
                ) & exclude_id
            )
        return cls.objects.none()


class BorrowerMergeRecord(models.Model):
    """
    Model to track merges between duplicate borrowers.
    """
    primary_borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='primary_merges')
    merged_borrower = models.ForeignKey(Borrower, on_delete=models.SET_NULL, null=True, related_name='secondary_merges')
    merged_borrower_data = models.JSONField(help_text="JSON data of the merged borrower before deletion")
    merged_at = models.DateTimeField(default=timezone.now)
    merged_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Merge: {self.merged_borrower} into {self.primary_borrower}"
