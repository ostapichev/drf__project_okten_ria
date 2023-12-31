import os

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from configs.celery import app

from core.dataclasses.user_dataclasses import UserDataClass
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken

from apps.users.models import UserModel as User

UserModel: User = get_user_model()


class EmailService:
    @staticmethod
    @app.task
    def __send_email(to: str, template_name: str, context: dict, subject=''):
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(subject, from_email=os.environ.get('EMAIL_HOST_USER'), to=[to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @classmethod
    def register_email(cls, user: UserDataClass):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        cls.__send_email.delay(user.email, 'register.html', {
            'name': user.profile.name,
            'url': url
        }, 'Register')

    @classmethod
    def recovery_email(cls, user: UserDataClass):
        token = JWTService.create_token(user, RecoveryToken)
        url = f'http://localhost:3000/recovery/{token}'
        cls.__send_email(user.email, 'recovery_password.html', {
            'name': user.profile.name,
            'url': url
        }, 'Recovery Password')

    @classmethod
    def content_email(cls, manager_user: UserDataClass, user: UserDataClass):
        cls.__send_email(manager_user.email, 'content_validate.html', {
            'manager_user': manager_user.profile.name,
            'email': user,
        }, 'Validate Content')
