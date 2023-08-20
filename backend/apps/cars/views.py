from django.http import Http404
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from .filters import CarFilter
from .models import BrandCarModel, CarModel, ModelCarModel
from .serializers import BrandCarSerializer, CarPhotoSerializer, CarSerializer, ModelCarSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class CarListView(GenericAPIView, ListModelMixin):
    """
        Get all cars
    """
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer
    filterset_class = CarFilter
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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
