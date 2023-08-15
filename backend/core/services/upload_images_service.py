import os.path
from uuid import uuid1

from core.dataclasses.car_dataclasses import CarDataClass
from core.dataclasses.user_dataclasses import ProfileDataClass


def upload_avatar(instance: ProfileDataClass, file: str) -> str:
    ext = file.split('.')[-1]
    return os.path.join(instance.surname, 'avatar', f'{uuid1()}.{ext}')


def upload_photo_car(instance: CarDataClass, file: str) -> str:
    ext = file.split('.')[-1]
    return os.path.join(instance.user.profile.surname, 'cars', f'{uuid1()}.{ext}')
