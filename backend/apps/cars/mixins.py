from django.http import Http404

from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.cars.models import BrandCarModel


class BaseMixinCarName(GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = None


class MixinListAddNameCar(BaseMixinCarName):
    model_class = None

    @staticmethod
    def __get_brand_or_404(brand_id):
        try:
            return BrandCarModel.objects.get(id=brand_id)
        except BrandCarModel.DoesNotExist:
            raise Http404

    def __validate_serializer(self):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def __add_brand(self):
        brand_name = self.request.data.get('brand_name')
        existing_brand = BrandCarModel.objects.filter(brand_name=brand_name).exists()
        if existing_brand:
            raise serializers.ValidationError("Brand with this name already exists.")
        return self.__validate_serializer()

    def get(self, request, id=None, *args, **kwargs):
        if id is None:
            items = BrandCarModel.objects.all()
        else:
            brand = self.__get_brand_or_404(id)
            items = self.model_class.objects.filter(brand=brand)
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id=None, *args, **kwargs):
        if id is None:
            serializer = self.__add_brand()
            serializer.save()
        else:
            brand_name = self.__get_brand_or_404(id)
            model_name = self.request.data.get('model_name')
            if self.model_class.objects.filter(brand=brand_name, model_name=model_name).exists():
                return Response("This model with this name already exists.", status=status.HTTP_400_BAD_REQUEST)
            serializer = self.__validate_serializer()
            serializer.save(brand=brand_name)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MixinUpdateNameCar(BaseMixinCarName):
    model_class = None

    @staticmethod
    def __get_object(pk, model_class):
        try:
            return model_class.objects.get(pk=pk)
        except model_class.DoesNotExist:
            raise Http404

    def patch(self, request, id, *args, **kwargs):
        model_class = self.model_class
        instance = self.__get_object(id, model_class)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id, *args, **kwargs):
        model_class = self.model_class
        instance = self.__get_object(id, model_class)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
