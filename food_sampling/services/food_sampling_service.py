from datetime import datetime
from ninja.errors import HttpError
from cycle.repositories.cycle_repo import CycleRepo
from food_sampling.repositories.food_sampling_repository import FoodSamplingRepository
from food_sampling.schemas import FoodSamplingCreateSchema
from food_sampling.models import FoodSampling
from pond.models import Pond
from cycle.models import Cycle
from pond_quality.api import CYCLE_NOT_ACTIVE
from user_profile.utils import get_supervisor

class FoodSamplingService:
    DATA_NOT_FOUND = "Data tidak ditemukan"
    INVALID_FOOD_QUANTITY = "Input kuantitas makanan tidak valid"
    UNAUTHORIZED_ACCESS = "Anda tidak memiliki akses untuk melihat data ini"

    def __init__(self, repository: FoodSamplingRepository):
        self.repository = repository

    def check_cycle_active(self, cycle: Cycle):
        today = datetime.now().date()
        if not (cycle.start_date <= today <= cycle.end_date):
            raise HttpError(400, self.DATA_NOT_FOUND)

    def authorize_user(self, user, pond: Pond):
        supervisor = get_supervisor(user)
        if pond.owner != supervisor:
            raise HttpError(401, self.UNAUTHORIZED_ACCESS)

    def get_food_sampling(self, cycle_id: str, pond_id: str, sampling_id: str, user) -> FoodSampling:
        cycle = self.repository.get_cycle(cycle_id)
        pond = self.repository.get_pond(pond_id)
        food_sampling = self.repository.get_food_sampling_by_id(sampling_id)

        self.check_cycle_active(cycle)

        if food_sampling.cycle != cycle or food_sampling.pond != pond:
            raise HttpError(404, self.DATA_NOT_FOUND)

        self.authorize_user(user, pond)
        return food_sampling

    def get_latest_food_sampling(self, cycle_id: str, pond_id: str, user) -> FoodSampling:
        cycle = self.repository.get_cycle(cycle_id)
        pond = self.repository.get_pond(pond_id)

        self.check_cycle_active(cycle)

        food_sampling = self.repository.get_latest_food_sampling(pond, cycle)
        if food_sampling is None:
            raise HttpError(404, self.DATA_NOT_FOUND)

        self.authorize_user(user, pond)
        return food_sampling

    def list_food_samplings(self, pond_id: str, user):
        cycle = CycleRepo.get_active_cycle(get_supervisor(user))
        pond = self.repository.get_pond(pond_id)

        if self.authorize_user(user, pond):
            raise HttpError(401, self.UNAUTHORIZED_ACCESS)
        if cycle is None:
            raise HttpError(404, CYCLE_NOT_ACTIVE)

        food_samplings = self.repository.list_food_samplings(cycle, pond)
        return {
            'food_samplings': food_samplings,
            'cycle_id': cycle.id
        }

    def create_food_sampling(self, pond_id: str, cycle_id: str, reporter_id: int, payload: FoodSamplingCreateSchema) -> FoodSampling:
        pond = self.repository.get_pond(pond_id)
        reporter = self.repository.get_reporter(reporter_id)
        cycle = self.repository.get_cycle(cycle_id)

        today = datetime.now().date()
        existing_food_sampling = self.repository.get_existing_food_sampling(cycle, pond, today)

        if existing_food_sampling:
            self.repository.delete_food_sampling(existing_food_sampling)

        try:
            food_sampling = self.repository.create_food_sampling(
                pond=pond,
                reporter=reporter,
                cycle=cycle,
                food_quantity=payload.food_quantity,
                recorded_at=payload.recorded_at
            )
        except ValueError:
            raise HttpError(400, self.INVALID_FOOD_QUANTITY)

        return food_sampling
