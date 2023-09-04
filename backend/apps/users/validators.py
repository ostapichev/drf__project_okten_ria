from django.contrib.auth import get_user_model

from core.services.email_service import EmailService

from apps.users.models import UserModel as User

UserModel: User = get_user_model()


class UserValidator:
    @staticmethod
    def validate_user(user_id):
        manager_user = UserModel.objects.get(is_manager=True)
        user = UserModel.objects.get(id=user_id)
        if not user.is_staff:
            user.is_active = False
            user.save()
            EmailService.content_email(manager_user, user.email)
        return user
