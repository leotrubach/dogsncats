from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.users.enums import UserRole
from . import models


class PetSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        owner = validated_data['owner']
        request = self.context['request']
        if request.user.role == UserRole.OWNER:
            if owner != request.user.owner:
                raise PermissionDenied("Pet owner cannot create pet for someone else")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'owner' in validated_data:
            if instance.owner != validated_data['owner']:
                if self.context['request'].user.role == UserRole.OWNER:
                    raise PermissionDenied("Pet owner user cannot modify `owner` field")
        return super().update(instance, validated_data)


class DogSerializer(PetSerializer):
    class Meta:
        model = models.Dog
        fields = '__all__'


class CatSerializer(PetSerializer):
    class Meta:
        model = models.Cat
        fields = '__all__'


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Owner
        fields = '__all__'
