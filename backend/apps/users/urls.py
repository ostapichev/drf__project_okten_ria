from django.urls import path

from .views import UserAddAvatarView, UserCarCreateView, UserCarUpdateDestroyView, UserListCreateView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user_list_create'),
    path('/avatar_user', UserAddAvatarView.as_view(), name='user_add_avatar'),
    path('/<int:pk>/cars', UserCarCreateView.as_view(), name='user_car_create'),
    path('/<int:user_id>/cars/<int:car_id>', UserCarUpdateDestroyView.as_view(), name='user_car_update_destroy'),
]
