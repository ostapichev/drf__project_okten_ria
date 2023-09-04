from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from core.services.email_service import EmailService

from ..cars.serializers import CarSerializer
from .models import CityModel, CountModel, ProfileModel
from .models import UserModel as User

UserModel: User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    def validate_location(self, value):
        try:
            city = CityModel.objects.get(name=value)
            return city.name
        except CityModel.DoesNotExist:
            raise serializers.ValidationError(
                "This city does not exist in the database. Please contact the site administrator.")

    class Meta:
        model = ProfileModel
        fields = ('id', 'name', 'surname', 'age', 'location', 'avatar')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    cars = CarSerializer(many=True, read_only=True)

    @transaction.atomic
    def create(self, validated_data: dict):
        profile_data = validated_data.pop('profile')
        profile = ProfileModel.objects.create(**profile_data)
        user = UserModel.objects.create_user(profile=profile, **validated_data)
        EmailService.register_email(user)
        return user

    class Meta:
        model = UserModel
        fields = (
            'id',
            'email',
            'password',
            'is_active',
            'is_premium',
            'is_staff',
            'is_manager',
            'is_superuser',
            'last_login',
            'created_at',
            'updated_at',
            'profile',
            'cars',
        )
        read_only_fields = (
            'id',
            'is_active',
            'is_premium',
            'is_staff',
            'is_superuser',
            'last_login',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('avatar',)
        extra_kwargs = {
            'avatar': {
                'required': True
            }
        }


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityModel
        fields = ('id', 'name')



