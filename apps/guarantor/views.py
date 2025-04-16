from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Guarantor
from .serializers import GuarantorSerializer

class GuarantorCreateView(generics.CreateAPIView):
    """
    Create a new guarantor
    """
    serializer_class = GuarantorSerializer
    permission_classes = [IsAuthenticated]

class GuarantorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a guarantor
    """
    queryset = Guarantor.objects.all()
    serializer_class = GuarantorSerializer
    permission_classes = [IsAuthenticated]
