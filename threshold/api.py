from ninja import Router
from cycle.models import Cycle
from pond.models import Pond
from threshold.utils import get_latest_pond_quality, validate_pond_quality_against_threshold
from ninja_jwt.authentication import JWTAuth

router = Router()

@router.get("/{cycle_id}/{pond_id}/", auth=JWTAuth(), response={200: dict})
def validate_data(request, cycle_id: str, pond_id: str):
    user = request.auth
    pond = Pond.objects.get(pond_id=pond_id)
    cycle = Cycle.objects.get(id=cycle_id)

    pond_quality = get_latest_pond_quality(user, pond, cycle)
    violations = validate_pond_quality_against_threshold(pond_quality)

    if violations:
        return {
            "healthy": False,
            "pond_quality_id": pond_quality.id,
            "violations": violations
        }

    return {
        "healthy": True,
        "pond_quality_id": pond_quality.id,
        "message": "Kualiats air kolam sesuai dengan standar"
    }