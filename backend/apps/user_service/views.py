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


class UserToAdminView(GenericAPIView):
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

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


class AdminToUserView(GenericAPIView):
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if user.is_staff:
            user.is_staff = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BlockUserView(GenericAPIView):
    permission_classes = (IsAdminUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if user.is_active:
            user.is_active = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UnBlockUserView(GenericAPIView):
    permission_classes = (IsAdminUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user: User = self.get_object()
        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BlockAminView(BlockUserView):
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UnBlockAminView(UnBlockUserView):
    permission_classes = (IsSuperUser,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserToPremium(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def patch(self, *args, **kwargs):
        current_user_id = self.request.user.pk
        pk = kwargs['pk']
        user: User = self.get_object()
        if not user.is_premium and current_user_id == pk:
            user.is_premium = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserToNotPremium(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        current_user_id = self.request.user.pk
        pk = kwargs['pk']
        user: User = self.get_object()
        if user.is_premium and current_user_id == pk:
            user.is_premium = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
