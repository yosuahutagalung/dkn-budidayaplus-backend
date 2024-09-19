from ninja import Router
from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import RefreshToken
from ninja.errors import HttpError

router = Router()

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            return RefreshToken(token).check_blacklist()
        except Exception:
            raise HttpError(401, "Invalid token")

@router.post("/login")
def login(request):
    return
    
@router.post("/register")
def register(request):
    return

@router.post("/logout")
def logout(request):
    return

@router.post("/refresh")    
def refresh(request):
    return

@router.post("/protected", auth=JWTAuth())
def protected(request):
    return {"message": "This is a protected route"}