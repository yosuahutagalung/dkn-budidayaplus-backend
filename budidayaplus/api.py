from authentication.controller import AuthController
from pond.controller import PondController
from fish_sampling.controller import FishSamplingController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

api.register_controllers(
  AuthController,
  PondController,  
  FishSamplingController,
)