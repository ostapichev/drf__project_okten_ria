from django.utils.decorators import method_decorator

from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema

from .filters import CarFilter
from .models import CarModel
from .serializers import CarPhotoSerializer, CarSerializer


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

