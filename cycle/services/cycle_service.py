from datetime import date
from typing import Literal
from django.contrib.auth.models import User
from cycle.utils import is_valid_fish_amount, is_valid_period
from cycle.repositories.cycle_repo import CycleRepo
from cycle.repositories.pond_fish_amount_repo import PondFishAmountRepo
from cycle.schemas import CycleInput
from cycle.models import Cycle
from cycle.signals import create_cycle_signal
from user_profile.utils import get_supervisor


class CycleService:
    @staticmethod
    def create_cycle(supervisor: User, payload: CycleInput):
        if CycleRepo.is_active_cycle_exist(supervisor, payload.start_date, payload.end_date):
            raise ValueError("Anda sudah memiliki siklus yang aktif")

        if not is_valid_period(payload.start_date, payload.end_date):
            raise ValueError("Periode siklus harus 60 hari")

        for pond_fish_amount in payload.pond_fish_amount:
            if (not is_valid_fish_amount(pond_fish_amount.fish_amount)):
                raise ValueError("Jumlah ikan harus lebih dari 0")

        cycle = CycleRepo.create(payload.start_date, payload.end_date, supervisor)
        PondFishAmountRepo.bulk_create(payload.pond_fish_amount, cycle)

        create_cycle_signal.send(sender=CycleService, instance=cycle, created=True)

        return cycle 

    @staticmethod
    def get_active_cycle(user: User):
        supervisor = get_supervisor(user)
        cycle = CycleRepo.get_active_cycle(supervisor)
        if cycle is None:
            raise ValueError("Siklus tidak ditemukan")
        return cycle

    @staticmethod
    def get_cycle_by_id(id: str):
        cycle = CycleRepo.get_cycle_by_id(id)
        if cycle is None:
            raise ValueError("Siklus tidak ditemukan")
        return cycle

    @staticmethod
    def get_cycle_past_or_future(user: User, date: date, direction: Literal['past', 'future']):
        supervisor = get_supervisor(user)
        return CycleRepo.get_cycle_past_or_future(supervisor, date, direction)

    @staticmethod
    def get_active_cycle_safe(user: User):
        supervisor = get_supervisor(user)
        cycle = CycleRepo.get_active_cycle_safe(supervisor)
        return cycle

    @staticmethod
    def get_stopped_cycle(user: User):
        supervisor = get_supervisor(user)
        return Cycle.objects.filter(supervisor=supervisor, is_stopped=True)

    @staticmethod
    def stop_cycle(cycle_id: str, supervisor: User):
        cycle = CycleRepo.get_cycle_by_id(cycle_id)
        if not cycle:
            raise ValueError("Siklus tidak ditemukan")
        CycleRepo.stop_cycle(cycle_id)
        return cycle
