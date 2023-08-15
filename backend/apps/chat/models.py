from django.contrib.auth import get_user_model
from django.db import models

from apps.users.models import UserModel as User

UserModel: User = get_user_model()


class ChatModel(models.Model):
    message = models.CharField(max_length=255)
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'chat'
