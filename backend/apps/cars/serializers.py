from rest_framework import serializers

from .models import BrandCarModel, CarModel, ModelCarModel


class CarSerializer(serializers.ModelSerializer):

    def validate_brand(self, data):
        try:
            car_name = self._kwargs['data']['model']
            car_brand = BrandCarModel.objects.get(brand=data)
            car_name = ModelCarModel.objects.get(brand_name=car_name)
            if car_name.brand_id == car_brand.id:
                return car_brand.brand
        except BrandCarModel.DoesNotExist:
            raise serializers.ValidationError(
                "This brand of the car does not exist in the database. "
                "Please contact the site administrator.")
        except ModelCarModel.DoesNotExist:
            raise serializers.ValidationError(
                "This model of the brand on the car does not exist in the database. "
                "Please contact the site administrator.")

    class Meta:
        model = CarModel
        fields = ('id', 'photo_car', 'brand', 'model', 'price', 'year', 'created_at', 'updated_at', 'user')


class CarPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('photo_car',)
        extra_kwargs = {
            'photo_car': {
                'required': True
            }
        }


class BrandCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandCarModel
        fields = ('id', 'brand')


class ModelCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCarModel
        fields = ('id', 'brand_name', 'brand_id')
