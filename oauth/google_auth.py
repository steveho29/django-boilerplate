from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from oauth.email_auth import EmailTokenObtainSerializer
from user.models import SOCIAL_AUTH_PLATFORM, User
from django.contrib.auth.base_user import BaseUserManager
import requests
import logging


class GoogleAuthSerializer(serializers.Serializer):
    credential = serializers.CharField(max_length=200)

class GoogleAuthView(APIView):
    serializer_class = GoogleAuthSerializer

    def post(self, request):
        payload = {'id_token': request.data.get("credential")}
        data = requests.get('https://oauth2.googleapis.com/tokeninfo', params=payload).json()
        
        logging.getLogger().error(data)

        if 'error' in data:
            content = {'message': 'Wrong google token or this google token is already expired.'}
            return Response(content)

        # Create user if not exist
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.set_password(BaseUserManager().make_random_password())
            user.email = data['email']
            user.social_auth = SOCIAL_AUTH_PLATFORM.GOOGLE
            user.email_verified = True
            user.first_name = data.get('given_name')
            user.last_name = data.get('family_name')
            user.avatar = data.get('picture')
            user.save()

        serializer = EmailTokenObtainSerializer()
        token = serializer.get_token(user)
        return Response({'access_token': str(token.access_token), 'refresh_token': str(token)})