from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from ninja.security import HttpBearer
from ninja.errors import HttpError
from django.contrib.auth.models import User

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token.payload.get("user_id")
            return User.objects.get(id=user_id)
        except TokenError:
            raise HttpError(401, "Token is invalid or expired")
