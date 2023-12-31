from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_premium', True)
        kwargs.setdefault('is_manager', False)
        if not kwargs['is_staff']:
            raise ValueError('Superuser must have is_staff')
        if not kwargs['is_superuser']:
            raise ValueError('Superuser must have is_superuser')
        user = self.create_user(email, password, **kwargs)
        return user

    def all_with_profiles(self):
        return self.select_related('profile')
