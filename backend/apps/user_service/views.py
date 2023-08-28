from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import no_body, swagger_auto_schema

from core.permissions.is_extra_user import IsSuperUser

from apps.users.models import UserModel as User
from apps.users.serializers import UserSerializer

UserModel: User = get_user_model()


class BaseUserServiceView(GenericAPIView):
    permission_classes = None
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserToAdminView(BaseUserServiceView):
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    @swagger_auto_schema(request_body=no_body)
    def patch(self, *args, **kwargs):
        user = self.get_object()
        if not user.is_staff:
            user.is_staff = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class AdminToUserView(BaseUserServiceView):
    permission_classes = (IsSuperUser,)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if user.is_staff:
            user.is_staff = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BlockUserView(BaseUserServiceView):
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if user.is_active:
            user.is_active = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UnBlockUserView(BaseUserServiceView):
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BlockAdminView(BlockUserView):
    permission_classes = (IsSuperUser,)


class UnBlockAdminView(UnBlockUserView):
    permission_classes = (IsSuperUser,)


class UserToPremiumView(BaseUserServiceView):
    permission_classes = (IsAuthenticated,)

    def patch(self, *args, **kwargs):
        current_user_id = self.request.user.pk
        pk = kwargs['pk']
        user: User = self.get_object()
        if not user.is_premium and current_user_id == pk:
            user.is_premium = True
            user.save()
        else:
            return Response("Not found")
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserToNotPremiumView(BaseUserServiceView):
    permission_classes = (IsAuthenticated,)

    def patch(self, *args, **kwargs):
        current_user_id = self.request.user.pk
        pk = kwargs['pk']
        user: User = self.get_object()
        if user.is_premium and current_user_id == pk:
            user.is_premium = False
            user.save()
        else:
            return Response("Not found")
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
