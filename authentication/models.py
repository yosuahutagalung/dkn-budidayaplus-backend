from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from ninja.security import HttpBearer
from ninja.errors import HttpError

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            AccessToken(token)
            return True
        except TokenError:
            raise HttpError(401, "Token is invalid or expired")
