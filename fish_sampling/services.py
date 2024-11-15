from datetime import datetime
from ninja.errors import HttpError
from .repositories import FishSamplingRepository
from fish_sampling.schemas import FishSamplingCreateSchema
from fish_sampling.models import FishSampling

class FishSamplingService:
    DATA_NOT_FOUND = "Data tidak ditemukan"
    INVALID_FISH_MEASUREMENTS = "Berat dan panjang ikan harus lebih dari 0"
    CYCLE_NOT_ACTIVE = "Siklus tidak aktif"

    def __init__(self, repository: FishSamplingRepository):
        self.repository = repository

    def create_fish_sampling(self, pond_id: str, cycle_id: str, reporter_id: int, payload: FishSamplingCreateSchema) -> FishSampling:
        pond = self.repository.get_pond(pond_id)
        reporter = self.repository.get_reporter(reporter_id)
        cycle = self.repository.get_cycle(cycle_id)

        today = datetime.now().date()
        if not (cycle.start_date <= today <= cycle.end_date):
            raise HttpError(400, self.CYCLE_NOT_ACTIVE)

        existing_fish_sampling = self.repository.get_existing_fish_sampling(cycle, pond, today)
        if existing_fish_sampling:
            self.repository.delete_fish_sampling(existing_fish_sampling)

        if payload.fish_weight <= 0 or payload.fish_length <= 0:
            raise HttpError(400, self.INVALID_FISH_MEASUREMENTS)

        try:
            fish_sampling = self.repository.create_fish_sampling(
                pond=pond,
                reporter=reporter,
                cycle=cycle,
                fish_weight=payload.fish_weight,
                fish_length=payload.fish_length,
            )
        except ValueError:
            raise HttpError(400, self.INVALID_FISH_MEASUREMENTS)

        return fish_sampling
    
    def get_latest_fish_sampling(self, cycle_id: str, pond_id: str, user) -> FishSampling:
        cycle = self.repository.get_cycle(cycle_id)
        pond = self.repository.get_pond(pond_id)

        today = datetime.now().date()
        if not (cycle.start_date <= today <= cycle.end_date):
            raise HttpError(400, self.CYCLE_NOT_ACTIVE)

        fish_sampling = self.repository.get_latest_fish_sampling(pond, cycle)
        if fish_sampling is None:
            raise HttpError(404, self.DATA_NOT_FOUND)

        return fish_sampling

    def list_fish_samplings(self, cycle_id: str, pond_id: str, user):
        cycle = self.repository.get_cycle(cycle_id)
        pond = self.repository.get_pond(pond_id)

        today = datetime.now().date()
        if not (cycle.start_date <= today <= cycle.end_date):
            raise HttpError(400, self.CYCLE_NOT_ACTIVE)

        return self.repository.list_fish_samplings(cycle, pond)