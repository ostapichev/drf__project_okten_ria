from django.urls import path

from .views import (
    BrandListAddView,
    BrandUpdateDestroyView,
    CarAddPhotoView,
    CarListView,
    ModelListAddView,
    ModelUpdateDestroyView,
)

urlpatterns = [
    path('', CarListView.as_view(), name='car_list'),
    path('/<int:user_id>/car_photo/<int:car_id>', CarAddPhotoView.as_view(), name='car_add_photo'),
    path('/car_brands_in_db', BrandListAddView.as_view(), name='list_car_brands_in_db'),
    path('/car_brands_in_db/<int:id>', BrandUpdateDestroyView.as_view(), name='update_destroy_car_brand_in_db'),
    path('/<int:id>/model_by_brand_in_db', ModelListAddView.as_view(), name='list_add_model_by_brand_in_db'),
    path('/<int:brand_id>/model_by_brand_in_db/<int:model_id>', ModelUpdateDestroyView.as_view(),
         name='update_destroy_model_by_brand_in_db'),
]
