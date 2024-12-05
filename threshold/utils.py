from django.core.exceptions import ObjectDoesNotExist
from ninja.errors import HttpError
from threshold.models import PondQualityThreshold
from pond_quality.models import PondQuality

DATA_NOT_FOUND = "Data tidak ditemukan"
GREEN = "healthy"
YELLOW = "moderate"
RED = "unhealthy"

def get_latest_pond_quality(user, pond, cycle):
    try:
        pond_quality = PondQuality.objects.filter(pond=pond, cycle=cycle).latest('recorded_at')
        return pond_quality
    except ObjectDoesNotExist:
        raise HttpError(404, DATA_NOT_FOUND)

def validate_pond_quality_against_threshold(pond_quality):
    try:
        threshold = PondQualityThreshold.objects.latest('id')
    except PondQualityThreshold.DoesNotExist:
        raise HttpError(500, "Threshold tidak ditemukan.")

    violations = []
    states = {}
    status = GREEN

    checks = [
        ("pH Level", "ph_level", pond_quality.ph_level, threshold.min_ph, threshold.max_ph),
        ("Salinity", "salinity", pond_quality.salinity, threshold.min_salinity, threshold.max_salinity),
        ("Temperature", "water_temperature", pond_quality.water_temperature, threshold.min_temperature, threshold.max_temperature),
        ("Clarity", "water_clarity", pond_quality.water_clarity, threshold.min_clarity, threshold.max_clarity),
        ("Circulation", "water_circulation", pond_quality.water_circulation, threshold.min_circulation, threshold.max_circulation),
        ("Dissolved Oxygen", "dissolved_oxygen", pond_quality.dissolved_oxygen, threshold.min_dissolved_oxygen, threshold.max_dissolved_oxygen),
        ("ORP", "orp", pond_quality.orp, threshold.min_orp, threshold.max_orp),
        ("Ammonia", "ammonia", pond_quality.ammonia, threshold.min_ammonia, threshold.max_ammonia),
        ("Nitrate", "nitrate", pond_quality.nitrate, threshold.min_nitrate, threshold.max_nitrate),
        ("Phosphate", "phosphate", pond_quality.phosphate, threshold.min_phosphate, threshold.max_phosphate),
    ]

    for field_name, key, value, min_val, max_val in checks:
        tolerance = threshold.tolerance_rate * (max_val - min_val)
        healthy_min = min_val - tolerance
        healthy_max = max_val + tolerance

        if value < healthy_min or value > healthy_max:
            states[key] = RED
            violations.append(f"{field_name} {value} diluar dari batas standar ({min_val} - {max_val}) dengan toleransi {int(threshold.tolerance_rate*100)}%.")
        elif min_val <= value <= max_val:
            states[key] = GREEN
        else:
            states[key] = YELLOW
    
    if violations:
        status = YELLOW
        
    if len(violations) > threshold.tolerance_rate * len(checks):
        status = RED

    return status, violations, states
