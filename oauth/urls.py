from django.urls import  path
from oauth.email_auth import EmailTokenObtainPairView, TokenRefreshView, TokenVerifyView
from oauth.google_auth import GoogleAuthView

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

urlpatterns = [
    path('', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify', TokenVerifyView.as_view(), name='token_verify'),
    path('google', GoogleAuthView.as_view(), name='google'),
]