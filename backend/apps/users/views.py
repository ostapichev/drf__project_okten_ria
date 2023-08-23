from django.contrib.auth import get_user_model
from django.http import Http404
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import Response

from drf_yasg.utils import swagger_auto_schema

from apps.users.models import CityModel
from apps.users.models import UserModel as User

from .filters import UserFilter
from .serializers import AvatarSerializer, CitySerializer, UserSerializer

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


class CityListAddView(GenericAPIView):
    """
        get:
            Get all Cities in db
        post:
            Add new city in db
    """
    queryset = CityModel.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = CitySerializer

    def get(self, *args, **kwargs):
        cities = CityModel.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        city_name = data.get('name')
        existing_city = CityModel.objects.filter(name=city_name).first()
        if existing_city:
            return Response("City with this name already exists.", status.HTTP_400_BAD_REQUEST)
        serializer = CitySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class CityUpdateDestroyView(GenericAPIView):
    """
        patch:
            Get all Cities in db
        delete:
            Add new city in db
    """
    queryset = CityModel.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = CitySerializer

    def patch(self, *args, **kwargs):
        pk = kwargs['id']
        data = self.request.data
        cities_data = CityModel.objects.filter(pk=pk)
        if not cities_data.exists():
            raise Http404()
        city = cities_data.get(id=pk)
        serializer = CitySerializer(city, data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        pk = kwargs['id']
        cities_data = CityModel.objects.filter(pk=pk)
        if not cities_data.exists():
            raise Http404()
        city = cities_data.get(id=pk)
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
