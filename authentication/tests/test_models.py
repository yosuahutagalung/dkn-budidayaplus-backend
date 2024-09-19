from django.test import TestCase
from rest_framework_simplejwt.tokens import AccessToken
from ninja.errors import HttpError
from ninja.testing import TestClient
from ninja import NinjaAPI
from authentication.models import JWTAuth
from authentication.api import router

class JWTAuthTestCase(TestCase):
    def setUp(self):
        self.api = NinjaAPI()
        self.auth = JWTAuth()
        self.client = TestClient(router)

    def test_authenticate_valid_token(self):
        token = str(AccessToken.for_user(self.create_user()))
        
        request = self.client.get('/protected', headers={'Authorization': f'Bearer {token}'})
        
        try:
            self.auth.authenticate(request, token)
            self.assertEqual(request.status_code, 200)
        except HttpError as e:
            self.fail(f"Authentication failed: {e}")

    def test_authenticate_invalid_token(self):
        invalid_token = "invalid_token"
        
        request = self.client.get('/protected', HTTP_AUTHORIZATION=f'Bearer {invalid_token}')
        
        with self.assertRaises(HttpError) as cm:
            self.auth.authenticate(request, invalid_token)
        
        self.assertEqual(cm.exception.status_code, 401)
        self.assertEqual(str(cm.exception), "Token is invalid or expired")

    def create_user(self):
        # Helper method to create a user for generating tokens
        from django.contrib.auth.models import User
        return User.objects.create_user(username='testuser', password='testpassword')
