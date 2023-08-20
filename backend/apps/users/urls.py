from django.urls import path

from .views import (
    CityAddDeleteListView,
    UserAddAvatarView,
    UserCarCreateView,
    UserCarUpdateDestroyView,
    UserListCreateView,
)

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user_list_create'),
    path('/avatar_user', UserAddAvatarView.as_view(), name='user_add_avatar'),
    path('/<int:pk>/cars', UserCarCreateView.as_view(), name='user_car_create'),
    path('/<int:user_id>/cars/<int:car_id>', UserCarUpdateDestroyView.as_view(), name='user_car_update_destroy'),
    path('/all_cities', CityAddDeleteListView.as_view(), name='all_city'),
    path('/add_city', CityAddDeleteListView.as_view(), name='add_city'),
    path('/delete_city/<int:id>', CityAddDeleteListView.as_view(), name='delete_city'),
]
