from datetime import datetime
from ninja.errors import HttpError
from pond_quality.repositories.pond_quality_repository import PondQualityRepository
from pond_quality.schemas import PondQualityInput
from pond_quality.models import PondQuality
from pond.models import Pond
from cycle.models import Cycle

class PondQualityService:
    DATA_NOT_FOUND = "Data tidak ditemukan"
    INVALID_POND_QUALITY = "Input kualitas pond tidak valid"
    CYCLE_NOT_ACTIVE = "Siklus tidak aktif"
    UNAUTHORIZED_ACCESS = "Anda tidak memiliki akses untuk melihat data ini"

    def __init__(self, repository: PondQualityRepository):
        self.repository = repository

    def check_cycle_active(self, cycle: Cycle):
        today = datetime.now().date()
        if not (cycle.start_date <= today <= cycle.end_date):
            raise HttpError(400, self.CYCLE_NOT_ACTIVE)

    def authorize_user(self, user, pond_quality: PondQuality, pond: Pond):
        if pond_quality.reporter != user or pond.owner != user:
            raise HttpError(401, self.UNAUTHORIZED_ACCESS)

    def get_pond_quality(self, cycle_id: str, pond_id: str, id: str, user) -> PondQuality:
        cycle = self.repository.get_cycle(cycle_id)
        pond = self.repository.get_pond(pond_id)
        pond_quality = self.repository.get_pond_quality_by_id(id)

        self.check_cycle_active(cycle)

        if pond_quality.cycle != cycle or pond_quality.pond != pond:
            raise HttpError(404, self.DATA_NOT_FOUND)

        self.authorize_user(user, pond_quality, pond)
        return pond_quality

    def get_latest_pond_quality(self, cycle_id: str, pond_id: str, user) -> PondQuality:
        cycle = self.repository.get_cycle(cycle_id)
        pond = self.repository.get_pond(pond_id)

        self.check_cycle_active(cycle)

        pond_quality = self.repository.get_latest_pond_quality(pond, cycle)
        if pond_quality is None:
            raise HttpError(404, self.DATA_NOT_FOUND)

        self.authorize_user(user, pond_quality, pond)
        return pond_quality

    def list_pond_qualities(self, cycle_id: str, pond_id: str, user):
        cycle = self.repository.get_cycle(cycle_id)
        pond = self.repository.get_pond(pond_id)

        self.check_cycle_active(cycle)

        if cycle.supervisor != user:
            raise HttpError(401, self.UNAUTHORIZED_ACCESS)

        return self.repository.list_pond_qualities(cycle, pond)

    def create_pond_quality(self, pond_id: str, cycle_id: str, reporter_id: int, payload: PondQualityInput) -> PondQuality:
        pond = self.repository.get_pond(pond_id)
        reporter = self.repository.get_reporter(reporter_id)
        cycle = self.repository.get_cycle(cycle_id)

        today = datetime.now().date()
        existing_pond_quality = self.repository.get_existing_pond_quality(cycle, pond, today)

        if existing_pond_quality:
            self.repository.delete_pond_quality(existing_pond_quality)

        try:
            pond_quality = self.repository.create_pond_quality(
                pond=pond,
                reporter=reporter,
                cycle=cycle,
                image_name = payload.image_name,
                ph_level = payload.ph_level,
                salinity = payload.salinity,
                water_temperature = payload.water_temperature,
                water_clarity = payload.water_clarity,
                water_circulation = payload.water_circulation,
                dissolved_oxygen = payload.dissolved_oxygen,
                orp = payload.orp,
                ammonia = payload.ammonia,
                nitrate = payload.nitrate,
                phosphate = payload.phosphate
            )
        except ValueError:
            raise HttpError(400, self.INVALID_POND_QUALITY)

        return pond_quality