from authentication.schemas import LoginSchema, RegisterSchema, RefreshSchema
from ninja import Router
from ninja.throttling import AnonRateThrottle
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.exceptions import TokenError
from ninja.errors import HttpError
from django.contrib.auth.models import User
from ninja_jwt.authentication import JWTAuth

router = Router()


@router.post("/login", throttle=AnonRateThrottle(rate="10/h"))
def login(request, data: LoginSchema):
    try:
        user = User.objects.get(username=data.phone_number)
        if not user.check_password(data.password):
            raise HttpError(404, "Pengguna tidak terdaftar atau kata sandi salah")

        refresh = RefreshToken.for_user(user)
        return {
            "message": "Login berhasil",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    except User.DoesNotExist:
        raise HttpError(404, "Pengguna tidak terdaftar atau kata sandi salah")


@router.post("/register")
def register(request, data: RegisterSchema):
    try:
        if User.objects.filter(username=data.phone_number).exists():
            raise HttpError(400, "Pengguna sudah terdaftar")

        user = User.objects.create_user(
            username=data.phone_number,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            is_staff=True
        )
        refresh = RefreshToken.for_user(user)
        return {
            "message": "Akun berhasil dibuat",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
    except Exception as e:
        raise HttpError(400, str(e))


@router.post("/refresh")
def refresh(request, data: RefreshSchema):
    try:
        refresh = RefreshToken(data.refresh)
        new_access_token = str(refresh.access_token)

        user_id = refresh.payload.get("user_id")
        if not User.objects.filter(id=user_id).exists():
            raise HttpError(401, "Pengguna tidak ditemukan atau token tidak valid")

        return {"access": new_access_token}
    except TokenError:
        raise HttpError(401, "Token invalid atau telah kadaluarsa")


@router.post("/validate", auth=JWTAuth())
def validate(request):
    return {"message": "Token valid"}


@router.get("/me", auth=JWTAuth())
def get_user_by_token(request):
    user = request.auth
    return {
        "id": user.id,
        "phone_number": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name
    }
