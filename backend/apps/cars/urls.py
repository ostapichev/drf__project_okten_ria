from django.urls import path

from .views import BrandAddDestroyListView, CarAddPhotoView, CarListView, ModelAddDestroyListView

urlpatterns = [
    path('', CarListView.as_view(), name='car_list'),
    path('/<int:user_id>/car_photo/<int:car_id>', CarAddPhotoView.as_view(), name='car_add_photo'),
    path('/all_car_brands', BrandAddDestroyListView.as_view(), name='all_car_brands'),
    path('/add_car_brand', BrandAddDestroyListView.as_view(), name='add_car_brand'),
    path('/delete_car_brand/<int:id>', BrandAddDestroyListView.as_view(), name='delete_car_brand'),
    path('/<int:id>/all_model_by_brand', ModelAddDestroyListView.as_view(), name='list_model_of_brand'),
    path('/<int:id>/add_model_by_brand', ModelAddDestroyListView.as_view(), name='add_model_of_brand'),
    path('/<int:brand_id>/add_model_by_brand/<int:model_id>', ModelAddDestroyListView.as_view(), name='delete_model_of_brand'),
]
