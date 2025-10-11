from django.db import transaction
from User.models import Address
from User.serializers import AddressSerializer
from rest_framework import permissions, viewsets


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.none()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        is_default = serializer.validated_data.get("is_default", False)
        with transaction.atomic():
            if is_default:
                Address.objects.filter(user=self.request.user, is_default=True).update(is_default=False)
            serializer.save(user=self.request.user)



