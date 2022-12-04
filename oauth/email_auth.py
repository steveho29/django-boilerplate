from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class EmailTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['last_login'] = str(user.last_login)
        token['is_active'] = user.is_active
        token['email_verified'] = user.email_verified
        return token

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainSerializer
