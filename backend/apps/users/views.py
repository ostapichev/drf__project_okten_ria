from django.contrib.auth import get_user_model
from django.http import Http404
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response

from drf_yasg.utils import swagger_auto_schema

from apps.users.models import UserModel as User

from ..cars.models import CarModel
from ..cars.serializers import CarSerializer
from .filters import UserFilter
from .serializers import AvatarSerializer, UserSerializer

UserModel: User = get_user_model()


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
@method_decorator(name='post', decorator=swagger_auto_schema(security=[]))
class UserListCreateView(ListCreateAPIView):
    """
        get:
            Get all users
        post:
            Create user.
    """
    serializer_class = UserSerializer
    queryset = UserModel.objects.all_with_profiles()
    filterset_class = UserFilter
    permission_classes = (AllowAny,)


class UserAddAvatarView(UpdateAPIView):
    """
        Add avatar of the user
    """
    serializer_class = AvatarSerializer
    http_method_names = ('put',)

    def get_object(self):
        return UserModel.objects.all_with_profiles().get(pk=self.request.user.pk).profile

    def perform_update(self, serializer):
        self.get_object().avatar.delete()
        super().perform_update(serializer)


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class UserCarCreateView(GenericAPIView):
    """
        get:
            Get car by id user id
        post:
            Create car by user id
    """
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)
        return (AllowAny(),)

    def get(self, *args, **kwargs):
        pk = kwargs['pk']
        if not UserModel.objects.filter(pk=pk).exists():
            raise Http404()
        cars = CarModel.objects.filter(user_id=pk)
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        current_user_id = self.request.user.pk
        pk = kwargs['pk']
        data = self.request.data
        serializer = CarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        if not UserModel.objects.filter(pk=pk).exists() or current_user_id != pk:
            raise Http404()
        cars = CarModel.objects.filter(user_id=pk)
        if len(cars) < 1 or self.request.user.is_premium:
            serializer.save(user_id=pk)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response('You must to buy the premium account')


class UserCarUpdateDestroyView(GenericAPIView):
    """
        put:
            Full update car by id
        patch:
            Partial update car by id
        delete:
            Delete car by id
    """
    queryset = UserModel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def put(self, *args, **kwargs):
        current_user_id = self.request.user.pk
        pk = kwargs['user_id']
        data = self.request.data
        cars_data = CarModel.objects.filter(user_id=pk)
        car = cars_data.get(id=kwargs['car_id'])
        serializer = CarSerializer(car, data)
        serializer.is_valid(raise_exception=True)
        if not UserModel.objects.filter(pk=pk).exists() or current_user_id != pk:
            raise Http404()
        serializer.save(user_id=pk)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        current_user_id = self.request.user.pk
        pk = kwargs['user_id']
        data = self.request.data
        cars_data = CarModel.objects.filter(user_id=pk)
        car = cars_data.get(id=kwargs['car_id'])
        serializer = CarSerializer(car, data, partial=True)
        serializer.is_valid(raise_exception=True)
        if not UserModel.objects.filter(pk=pk).exists() or current_user_id != pk:
            raise Http404()
        serializer.save(user_id=pk)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        current_user_id = self.request.user.pk
        pk = kwargs['user_id']
        cars_data = CarModel.objects.filter(user_id=pk)
        car = cars_data.get(id=kwargs['car_id'])
        if current_user_id != pk:
            raise Http404()
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



