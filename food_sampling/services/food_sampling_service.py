from datetime import datetime
from ninja.errors import HttpError
from food_sampling.repositories.food_sampling_repository import FoodSamplingRepository
from food_sampling.schemas import FoodSamplingCreateSchema
from food_sampling.models import FoodSampling

class FoodSamplingService:
    DATA_NOT_FOUND = "Data tidak ditemukan"
    INVALID_FOOD_QUANTITY = "Input kuantitas makanan tidak valid"

    def __init__(self, repository: FoodSamplingRepository):
        self.repository = repository

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
