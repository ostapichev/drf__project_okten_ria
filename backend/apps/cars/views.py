from django.contrib.auth import get_user_model
from django.http import Http404
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from apps.users.models import UserModel as User

from .models import BrandCarModel, CarModel, ModelCarModel
from .serializers import BrandCarSerializer, CarPhotoSerializer, CarSerializer, ModelCarSerializer

UserModel: User = get_user_model()


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class AllCarsListView(GenericAPIView, ListModelMixin):
    """
        Get all cars
    """
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class CarListView(GenericAPIView):
    """
        Get car by id user
    """
    serializer_class = CarSerializer
    queryset = UserModel.objects.all()
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        pk = kwargs['pk']
        if not UserModel.objects.filter(pk=pk).exists():
            raise Http404()
        cars = CarModel.objects.filter(user_id=pk)
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class CarCreateView(GenericAPIView):
    """
        Create car from user
    """
    serializer_class = CarSerializer
    queryset = UserModel.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        current_user_id = self.request.user.pk
        data = self.request.data
        serializer_data = CarSerializer.validate_name_create_car(data)
        serializer = CarSerializer.validate_data(serializer_data)
        cars = CarModel.objects.filter(user_id=current_user_id)
        if len(cars) < 1 or self.request.user.is_premium:
            serializer.save(user_id=current_user_id)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response('You must to buy the premium account')


class CarAddPhotoView(UpdateAPIView):
    """
        Add photo for the car
    """
    serializer_class = CarPhotoSerializer
    http_method_names = ('put',)

    def get_object(self):
        return CarModel.my_object.all_with_cars().get(pk=self.kwargs['car_id'])

    def perform_update(self, serializer):
        self.get_object().photo_car.delete()
        super().perform_update(serializer)


class CarUpdateDestroyView(GenericAPIView):
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
    serializer_class = CarSerializer

    def get_object(self, car_id):
        current_user_id = self.request.user.pk
        try:
            car = CarModel.objects.get(id=car_id, user_id=current_user_id)
        except CarModel.DoesNotExist:
            raise Http404()
        return car

    def put(self, *args, **kwargs):
        car = self.get_object(kwargs['id'])
        serializer = CarSerializer.validate_and_save_car(car, self.request.data)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        car = self.get_object(kwargs['id'])
        serializer = CarSerializer.validate_and_save_car(car, self.request.data, partial=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        car = self.get_object(kwargs['id'])
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BrandListAddView(GenericAPIView):
    """
        get:
            Get all brands of cars
        post:
            Add brand of car
    """
    permission_classes = (IsAdminUser,)
    serializer_class = BrandCarSerializer

    def get(self, *args, **kwargs):
        brands = BrandCarModel.objects.all()
        serializer = BrandCarSerializer(brands, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        brand = data.get('brand_name')
        existing_brand = BrandCarModel.objects.filter(brand_name=brand).first()
        if existing_brand:
            return Response("Brand with this name already exists.", status.HTTP_400_BAD_REQUEST)
        serializer = BrandCarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class BrandUpdateDestroyView(GenericAPIView):
    """
        patch:
            Update the brand
        delete:
            Delete the brand
    """
    permission_classes = (IsAdminUser,)
    serializer_class = BrandCarSerializer

    def patch(self, *args, **kwargs):
        brand_id = kwargs['id']
        data = self.request.data
        brand_data = BrandCarModel.objects.filter(id=brand_id)
        if not brand_data.exists():
            raise Http404()
        brand = brand_data.get(id=brand_id)
        serializer = BrandCarSerializer(brand, data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        brand_id = kwargs['id']
        brand_data = BrandCarModel.objects.filter(pk=brand_id)
        if not brand_data.exists():
            raise Http404()
        brand = brand_data.get(id=brand_id)
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ModelListAddView(GenericAPIView):
    """
        get:
            Get all model by brand of cars
        post:
            Add model by brand of car
    """
    permission_classes = (IsAdminUser,)
    serializer_class = ModelCarSerializer

    def get(self, *args, **kwargs):
        model_id = kwargs['id']
        if not BrandCarModel.objects.filter(id=model_id).exists():
            raise Http404()
        name_model = ModelCarModel.objects.filter(brand_id=model_id)
        serializer = ModelCarSerializer(name_model, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        brand_id = kwargs['id']
        data = self.request.data
        model_name = data.get('model_name')
        existing_model_name = ModelCarModel.objects.filter(model_name=model_name).first()
        if existing_model_name:
            return Response("This model with this name already exists.", status.HTTP_400_BAD_REQUEST)
        serializer = ModelCarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        exists = BrandCarModel.objects.filter(id=brand_id).exists()
        if not exists:
            raise Http404
        serializer.save(brand_id=brand_id)
        return Response(serializer.data, status.HTTP_201_CREATED)


class ModelUpdateDestroyView(GenericAPIView):
    """
        patch:
            Update model by brand of car
        delete:
            Delete model by brand of car
    """
    permission_classes = (IsAdminUser,)
    serializer_class = ModelCarSerializer

    def patch(self, *args, **kwargs):
        model_id = kwargs['model_id']
        data = self.request.data
        model_data = ModelCarModel.objects.filter(id=model_id)
        if not model_data.exists():
            raise Http404()
        model = model_data.get(id=model_id)
        serializer = ModelCarSerializer(model, data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        model_id = kwargs['model_id']
        model_data = ModelCarModel.objects.filter(pk=model_id)
        if not model_data.exists():
            raise Http404()
        model = model_data.get(id=model_id)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
