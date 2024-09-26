from ninja import NinjaAPI
from authentication.api import router as auth_router
from pond.api import router as pond_router
from fish_sampling.api import router as fish_sampling_router

api = NinjaAPI()

api.add_router("/auth/", auth_router)
api.add_router("/pond/", pond_router)
api.add_router("/fish-sampling/", fish_sampling_router)