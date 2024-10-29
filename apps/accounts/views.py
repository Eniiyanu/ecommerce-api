from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Address
from .serializers import UserSerializer, AddressSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return User.objects.filter(id=self.request.user.id)
        return super().get_queryset()

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def default(self, request):
        address = self.get_queryset().filter(is_default=True).first()
        if address:
            serializer = self.get_serializer(address)
            return Response(serializer.data)
        return Response(
            {"detail": "No default address found."}, 
            status=status.HTTP_404_NOT_FOUND
        )