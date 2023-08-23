from django.urls import path

from .views import CityListAddView, CityUpdateDestroyView, UserAddAvatarView, UserListCreateView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user_list_create'),
    path('/avatar_user', UserAddAvatarView.as_view(), name='user_add_avatar'),
    path('/cities_in_db', CityListAddView.as_view(), name='list_add_city'),
    path('/cities_in_db/<int:id>', CityUpdateDestroyView.as_view(), name='update_destroy_city'),
]
