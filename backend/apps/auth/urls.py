from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.auth.views import ActivateUserView, AuthTokenView, MeView, RecoveryPasswordRequestView, RecoveryPasswordView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='auth_login'),
    path('/activate/<str:token>', ActivateUserView.as_view(), name='activate_user_view'),
    path('/refresh', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('/recovery_password', RecoveryPasswordRequestView.as_view(), name='recovery_password_request'),
    path('/recovery_password/<str:token>', RecoveryPasswordView.as_view(), name='recovery_password_view'),
    path('/me', MeView.as_view(), name='me_view'),
    path('/socket_token', AuthTokenView.as_view(), name='socket_token_view')
]