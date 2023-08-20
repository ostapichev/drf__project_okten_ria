from django.urls import path

from .views import (
    AdminToUserView,
    BlockAminView,
    BlockUserView,
    UnBlockAminView,
    UnBlockUserView,
    UserToAdminView,
    UserToNotPremium,
    UserToPremium,
)

urlpatterns = [
    path('/<int:pk>/to_admin', UserToAdminView.as_view(), name='user_to_admin'),
    path('/<int:pk>/to_user', AdminToUserView.as_view(), name='admin_to_user'),
    path('/<int:pk>/block_user', BlockUserView.as_view(), name='block_user'),
    path('/<int:pk>/unblock_user', UnBlockUserView.as_view(), name='unblock_user'),
    path('/<int:pk>/block_admin', BlockAminView.as_view(), name='block_admin'),
    path('/<int:pk>/unblock_admin', UnBlockAminView.as_view(), name='unblock_admin'),
    path('/<int:pk>/to_premium', UserToPremium.as_view(), name='user_to_premium'),
    path('/<int:pk>/to_not_premium', UserToNotPremium.as_view(), name='user_to_not_premium'),
]
