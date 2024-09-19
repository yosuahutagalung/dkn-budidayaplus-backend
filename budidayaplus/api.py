from ninja import NinjaAPI
from authentication.api import router as auth_router

api = NinjaAPI()

api.add_router("/auth/", auth_router)