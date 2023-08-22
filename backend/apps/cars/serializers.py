from rest_framework import serializers

from .models import BrandCarModel, CarModel, ModelCarModel


class CarSerializer(serializers.ModelSerializer):

    def post(self, request, *args, **kwargs):
        print(self._kwargs['data']['model'])

    def put(self, request, *args, **kwargs):
        print(self.instance.model)

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
