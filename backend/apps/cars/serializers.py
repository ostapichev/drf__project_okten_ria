from django.contrib.auth import get_user_model
from django.db.models import F

from rest_framework import serializers
from rest_framework.response import Response

from apps.users.models import CountModel
from apps.users.models import UserModel as User

from ..users.validators import UserValidator
from .models import BrandCarModel, CarModel, ModelCarModel
from .validators import CarValidator

UserModel: User = get_user_model()


class CountValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountModel()
        fields = ('id', 'count', 'user_id')


class CarSerializer(serializers.ModelSerializer):
    @staticmethod
    def __validate_name_car(brand, model):
        msg_call = "Please contact the site manager."
        try:
            car_brand = BrandCarModel.objects.get(brand_name=brand)
            car_model = ModelCarModel.objects.get(model_name=model)
            if car_model.brand_id == car_brand.id:
                return car_brand.brand_name
            raise serializers.ValidationError(
                f'This model of the car does not exist in the brand. {msg_call}')
        except BrandCarModel.DoesNotExist:
            raise serializers.ValidationError(
                f'This brand of the car does not exist in the database. {msg_call}')
        except ModelCarModel.DoesNotExist:
            raise serializers.ValidationError(
                f'This model of the brand on the car does not exist in the database. {msg_call}')

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

    @staticmethod
    def validate_name_create_car(data):
        try:
            CarSerializer.__validate_name_car(data['brand'], data['model'])
        except KeyError:
            return Response('You must specify the brand and model')
        return CarSerializer(data=data)

    @staticmethod
    def validate_data(serializer, user_id):
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            errors = e.detail
            if errors['content'][0] == CarValidator.msg_bad_words:
                content_count, created = CountModel.objects.get_or_create(user_id=user_id, defaults={"count": 0})
                if not created:
                    content_count.count = F('count') + 1
                    content_count.save()
                count_content = CountModel.objects.filter(user_id=user_id)
                if count_content[0].count > 2:
                    UserValidator.validate_user(user_id)
                    content_count.delete()
            raise e
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
