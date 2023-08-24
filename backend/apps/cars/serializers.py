from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.response import Response

from core.enums.regex_enum import RegExEnum

from apps.users.models import UserModel as User

from .models import BrandCarModel, CarModel, ModelCarModel

UserModel: User = get_user_model()


class CarSerializer(serializers.ModelSerializer):
    @staticmethod
    def __validate_name_car(brand, model):
        msg = "Please contact the site manager."
        try:
            car_brand = BrandCarModel.objects.get(brand_name=brand)
            car_model = ModelCarModel.objects.get(model_name=model)
            if car_model.brand_id == car_brand.id:
                return car_brand.brand_name
            raise serializers.ValidationError(
                f'This model of the car does not exist in the brand. {msg}')
        except BrandCarModel.DoesNotExist:
            raise serializers.ValidationError(
                f'This brand of the car does not exist in the database. {msg}')
        except ModelCarModel.DoesNotExist:
            raise serializers.ValidationError(
                f'This model of the brand on the car does not exist in the database. {msg}')

    @staticmethod
    def validate_name_create_car(data):
        try:
            CarSerializer.__validate_name_car(data['brand'], data['model'])
        except KeyError:
            return Response('You must specify the brand and model')
        return CarSerializer(data=data)

    @staticmethod
    def validate_data(serializer):
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            errors = e.detail
            if errors['content'][0] == RegExEnum.CONTENT.msg:
                print(errors['content'][0])
            raise e
        return serializer

    @staticmethod
    def validate_and_save_car(car, data, partial=False):
        if 'brand' in data:
            try:
                CarSerializer.__validate_name_car(data['brand'], data['model'])
            except KeyError:
                CarSerializer.__validate_name_car(data['brand'], car.model)
        else:
            try:
                CarSerializer.__validate_name_car(car.brand, data['model'])
            except KeyError:
                pass
        serializer = CarSerializer(car, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=car.user_id)
        return serializer

    class Meta:
        model = CarModel
        fields = ('id', 'photo_car', 'brand', 'model', 'price', 'year', 'content', 'created_at', 'updated_at', 'user')


class CarPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('photo_car',)
        extra_kwargs = {
            'photo_car': {
                'required': True
            }
        }


class ModelCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCarModel
        fields = ('id', 'model_name')


class BrandCarSerializer(serializers.ModelSerializer):
    model = ModelCarSerializer(many=True, read_only=True)

    class Meta:
        model = BrandCarModel
        fields = ('id', 'brand_name', 'model')
