from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    loan_type = models.CharField(max_length=50)
    min_loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    max_loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    min_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    max_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    min_term_months = models.IntegerField()
    max_term_months = models.IntegerField()
    establishment_fee = models.DecimalField(max_digits=15, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.loan_type})"


class ProductDocumentRequirement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='document_requirements')
    document_type = models.CharField(max_length=100)
    description = models.TextField()
    is_mandatory = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.document_type} for {self.product.name}"
