from rest_framework import viewsets

from apps.users.enums import UserRole
from .serializers import CatSerializer, DogSerializer, OwnerSerializer
from . import models


class CatViewSet(viewsets.ModelViewSet):
    queryset = models.Cat.objects.all()
    serializer_class = CatSerializer


class DogViewSet(viewsets.ModelViewSet):
    queryset = models.Dog.objects.all()
    serializer_class = DogSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = models.Owner.objects.all()
    serializer_class = OwnerSerializer
