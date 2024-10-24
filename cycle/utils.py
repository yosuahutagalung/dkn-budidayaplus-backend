from datetime import date
from cycle.models import Cycle

def is_cycle_active(cycle: Cycle):
    today = date.today()
    return cycle.start_date <= today <= cycle.end_date

def is_valid_period(start_date: date, end_date: date):
    return (end_date - start_date).days == 60

def is_valid_fish_amount(fish_amount: int):
    return fish_amount > 0