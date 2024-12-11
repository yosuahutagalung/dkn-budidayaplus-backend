from ninja import Schema, Field
from pydantic import UUID4
from typing import Optional, List
from datetime import datetime

from user_profile.schemas import UserSchema

class PondQualityInput(Schema):
    image_name: Optional[str] = ''
    ph_level: float
    salinity: float
    water_temperature: float
    water_clarity : float
    water_circulation: float
    dissolved_oxygen: float
    orp: float
    ammonia: float
    nitrate: float
    phosphate: float


class PondQualityOutput(Schema):
    id: UUID4
    cycle: UUID4 = Field(None, alias="cycle.id")
    pond: UUID4 = Field(None, alias="pond.pond_id")
    reporter: UserSchema
    recorded_at: datetime
    image_name: Optional[str] = ''
    ph_level: float
    salinity: float
    water_temperature: float
    water_clarity : float
    water_circulation: float
    dissolved_oxygen: float
    orp: float
    ammonia: float
    nitrate: float
    phosphate: float

class PondQualityHistory(Schema):
    pond_qualities: List[PondQualityOutput]
    cycle_id: UUID4
