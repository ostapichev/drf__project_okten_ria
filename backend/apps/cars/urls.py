from django.urls import path

from .views import CarAddPhotoView, CarListView

urlpatterns = [
    path('', CarListView.as_view(), name='car_list'),
    path('/<int:user_id>/car_photo/<int:car_id>', CarAddPhotoView.as_view(), name='car_add_photo'),
]