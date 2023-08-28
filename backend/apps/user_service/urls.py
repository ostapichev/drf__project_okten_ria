from django.urls import path

from .views import (
    AdminToUserView,
    BlockAdminView,
    BlockUserView,
    UnBlockAdminView,
    UnBlockUserView,
    UserToAdminView,
    UserToNotPremiumView,
    UserToPremiumView,
)

urlpatterns = [
    path('/<int:pk>/to_admin', UserToAdminView.as_view(), name='user_to_admin'),
    path('/<int:pk>/to_user', AdminToUserView.as_view(), name='admin_to_user'),
    path('/<int:pk>/block_user', BlockUserView.as_view(), name='block_user'),
    path('/<int:pk>/unblock_user', UnBlockUserView.as_view(), name='unblock_user'),
    path('/<int:pk>/block_admin', BlockAdminView.as_view(), name='block_admin'),
    path('/<int:pk>/unblock_admin', UnBlockAdminView.as_view(), name='unblock_admin'),
    path('/<int:pk>/to_premium', UserToPremiumView.as_view(), name='user_to_premium'),
    path('/<int:pk>/to_not_premium', UserToNotPremiumView.as_view(), name='user_to_not_premium'),
]
