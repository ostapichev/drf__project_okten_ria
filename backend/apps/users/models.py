from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.db import models

from core.enums.regex_enum import RegExEnum
from core.models import BaseModel
from core.services.upload_images_service import upload_avatar

from .managers import UserManager


class ProfileModel(BaseModel):
    name = models.CharField(max_length=50, validators=(
        validators.RegexValidator(RegExEnum.NAME.pattern, RegExEnum.NAME.msg),
    ))
    surname = models.CharField(max_length=50, validators=(
        validators.RegexValidator(RegExEnum.SURNAME.pattern, RegExEnum.SURNAME.msg),
    ))
    age = models.IntegerField(validators=(
        validators.MinValueValidator(16),
        validators.MaxValueValidator(150)
    ))
    avatar = models.ImageField(upload_to=upload_avatar, blank=True)
    location = models.CharField(max_length=30, validators=(
        validators.RegexValidator(RegExEnum.NAME.pattern, RegExEnum.NAME.msg),
    ))

    class Meta:
        db_table = 'profile'
        ordering = ('id', 'name', 'surname', 'age')


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True, validators=(
        validators.RegexValidator(RegExEnum.EMAIL.pattern, RegExEnum.EMAIL.msg),
    ))
    password = models.CharField(max_length=128, validators=(
        validators.RegexValidator(RegExEnum.PASSWORD.pattern, RegExEnum.PASSWORD.msg),
    ))
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    objects = UserManager()
    profile = models.OneToOneField(ProfileModel, on_delete=models.CASCADE, related_name='user', null=True)
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'auth_user'
        ordering = ('id',)


class CityModel(models.Model):
    name = models.CharField(max_length=30, validators=(
        validators.RegexValidator(RegExEnum.NAME.pattern, RegExEnum.NAME.msg),
    ))

    class Meta:
        db_table = 'cities'
        ordering = ('id', 'name')


class CountModel(models.Model):
    count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='count', null=True)

    class Meta:
        db_table = 'count_validate'
        ordering = ('id', 'count')
