from datetime import datetime

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from core.enums.regex_enum import RegExEnum
from core.models import BaseModel
from core.services.upload_images_service import upload_photo_car

from apps.users.models import UserModel as User

from .managers import CarManager

UserModel: User = get_user_model()


class CarModel(BaseModel):
    brand = models.CharField(max_length=25, validators=(
        validators.RegexValidator(RegExEnum.BRAND.pattern, RegExEnum.BRAND.msg),
    ))
    model = models.CharField(max_length=25, validators=(
        validators.RegexValidator(RegExEnum.MODEL.pattern, RegExEnum.BRAND.msg),
    ))
    price = models.IntegerField(validators=(
        validators.MinValueValidator(0),
        validators.MaxValueValidator(1000000)
    ))
    year = models.IntegerField(validators=(
        validators.MinValueValidator(1990),
        validators.MaxValueValidator(datetime.now().year)
    ))
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cars')
    objects = models.Manager()
    my_object = CarManager()
    photo_car = models.ImageField(upload_to=upload_photo_car, blank=True)

    class Meta:
        db_table = 'cars'
        ordering = ('id',)


class BrandCarModel(models.Model):
    brand = models.CharField(max_length=25, validators=(
        validators.RegexValidator(RegExEnum.BRAND.pattern, RegExEnum.BRAND.msg),
    ))

    class Meta:
        db_table = 'car_brands'
        ordering = ('id',)


class ModelCarModel(models.Model):
    brand_name = models.CharField(max_length=25, validators=(
        validators.RegexValidator(RegExEnum.BRAND.pattern, RegExEnum.BRAND.msg),
    ))
    brand = models.ForeignKey(BrandCarModel, on_delete=models.PROTECT, related_name='model', null=True)

    class Meta:
        db_table = 'car_models'
        ordering = ('id',)
