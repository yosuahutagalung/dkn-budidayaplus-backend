from django.core.exceptions import ObjectDoesNotExist
from ninja.errors import HttpError
from threshold.models import PondQualityThreshold
from pond_quality.models import PondQuality

DATA_NOT_FOUND = "Data tidak ditemukan"

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

    checks = [
        ("pH Level", pond_quality.ph_level, threshold.min_ph, threshold.max_ph),
        ("Salinitas", pond_quality.salinity, threshold.min_salinity, threshold.max_salinity),
        ("Suhu", pond_quality.water_temperature, threshold.min_temperature, threshold.max_temperature),
        ("Kecerahan", pond_quality.water_clarity, threshold.min_clarity, threshold.max_clarity),
        ("Sirkulasi", pond_quality.water_circulation, threshold.min_circulation, threshold.max_circulation),
        ("Kadar Oksigen", pond_quality.dissolved_oxygen, threshold.min_dissolved_oxygen, threshold.max_dissolved_oxygen),
        ("ORP", pond_quality.orp, threshold.min_orp, threshold.max_orp),
        ("Kadar Amonia", pond_quality.ammonia, threshold.min_ammonia, threshold.max_ammonia),
        ("Kadar Nitrat", pond_quality.nitrate, threshold.min_nitrate, threshold.max_nitrate),
        ("Kadar Fosfat", pond_quality.phosphate, threshold.min_phosphate, threshold.max_phosphate),
    ]

    for field, value, min_val, max_val in checks:
        if not (min_val <= value <= max_val):
            violations.append(f"{field}: {value} - Tidak sesuai batas standar ({min_val} - {max_val}).")

    return violations