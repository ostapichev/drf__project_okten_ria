from rest_framework import serializers

from apps.cars.models import BrandCarModel, ModelCarModel


def validate_name_car(brand, model):
    try:
        car_brand = BrandCarModel.objects.get(brand_name=brand)
        car_model = ModelCarModel.objects.get(model_name=model)
        if car_model.brand_id == car_brand.id:
            return car_brand.brand_name
        raise serializers.ValidationError(
            "This model of the car does not exist in the brand. "
            "Please contact the site administrator.")
    except BrandCarModel.DoesNotExist:
        raise serializers.ValidationError(
            "This brand of the car does not exist in the database. "
            "Please contact the site administrator.")
    except ModelCarModel.DoesNotExist:
        raise serializers.ValidationError(
            "This model of the brand on the car does not exist in the database. "
            "Please contact the site administrator.")