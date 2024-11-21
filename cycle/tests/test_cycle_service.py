from django.test import TestCase
from unittest.mock import MagicMock, patch
from cycle.schemas import CycleInput, PondFishAmountInput
from cycle.services.cycle_service import CycleService
from django.contrib.auth.models import User
from datetime import date, timedelta
from cycle.models import Cycle
import uuid


class CycleServiceTest(TestCase):
    def setUp(self):
        self.data_input = CycleInput(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            pond_fish_amount=[
                PondFishAmountInput(pond_id=uuid.uuid4(), fish_amount=10),
            ]
        )
        self.supervisor = MagicMock()
        self.user = User.objects.create_user(username='08123456789', password='test1234')

        patchers = [
            patch('cycle.repositories.cycle_repo.CycleRepo.is_active_cycle_exist'),
            patch('cycle.repositories.pond_fish_amount_repo.PondFishAmountRepo.bulk_create'),
            patch('cycle.repositories.cycle_repo.CycleRepo.create'),
            patch('cycle.repositories.cycle_repo.CycleRepo.get_cycle_by_id'),
            patch('cycle.repositories.cycle_repo.CycleRepo.stop_cycle'),
        ]

        self.mock_is_active_cycle_exist = patchers[0].start()
        self.mock_bulk_create_pfa = patchers[1].start()
        self.mock_create_cycle = patchers[2].start()
        self.mock_get_cycle_by_id = patchers[3].start()
        self.mock_stop_cycle = patchers[4].start()

        for patcher in patchers:
            self.addCleanup(patcher.stop)

    def test_create_cycle(self):
        self.mock_is_active_cycle_exist.return_value = False
        self.mock_create_cycle.return_value = MagicMock()

        cycle = CycleService.create_cycle(self.supervisor, self.data_input)

        self.assertEqual(self.mock_bulk_create_pfa.call_count, 1)
        self.assertEqual(self.mock_create_cycle.call_count, 1)
        self.assertEqual(cycle, self.mock_create_cycle.return_value)
        self.mock_bulk_create_pfa.assert_called_with(self.data_input.pond_fish_amount, self.mock_create_cycle.return_value)
        self.mock_is_active_cycle_exist.assert_called_with(self.supervisor, self.data_input.start_date, self.data_input.end_date)
        self.mock_create_cycle.assert_called_with(self.data_input.start_date, self.data_input.end_date, self.supervisor)


    def test_create_active_cycle_exists(self):
        self.mock_is_active_cycle_exist.return_value = True

        with self.assertRaises(ValueError) as context:
            CycleService.create_cycle(self.supervisor, self.data_input)

        self.assertEqual(self.mock_bulk_create_pfa.call_count, 0)
        self.assertEqual(self.mock_create_cycle.call_count, 0)
        self.assertEqual(self.mock_is_active_cycle_exist.call_count, 1)
        self.assertEqual(str(context.exception), "Anda sudah memiliki siklus yang aktif")
        self.mock_is_active_cycle_exist.assert_called_with(self.supervisor, self.data_input.start_date, self.data_input.end_date)


    def test_create_invalid_date_lt(self):
        self.mock_is_active_cycle_exist.return_value = False
        self.data_input.end_date -= timedelta(days=30)

        with self.assertRaises(ValueError) as context:
            CycleService.create_cycle(self.supervisor, self.data_input)

        self.assertEqual(self.mock_bulk_create_pfa.call_count, 0)
        self.assertEqual(self.mock_create_cycle.call_count, 0)
        self.assertEqual(str(context.exception), "Periode siklus harus 60 hari")


    def test_create_invalid_date_gt(self):
        self.mock_is_active_cycle_exist.return_value = False
        self.data_input.end_date += timedelta(days=1)

        with self.assertRaises(ValueError) as context:
            CycleService.create_cycle(self.supervisor, self.data_input)

        self.assertEqual(self.mock_bulk_create_pfa.call_count, 0)
        self.assertEqual(self.mock_create_cycle.call_count, 0)
        self.assertEqual(str(context.exception), "Periode siklus harus 60 hari")


    def test_create_invalid_fish_amount(self):
        self.mock_is_active_cycle_exist.return_value = False
        self.data_input.pond_fish_amount[0].fish_amount = 0

        with self.assertRaises(ValueError) as context:
            CycleService.create_cycle(self.supervisor, self.data_input)

        self.assertEqual(str(context.exception), "Jumlah ikan harus lebih dari 0")
        self.assertEqual(self.mock_bulk_create_pfa.call_count, 0)
        self.assertEqual(self.mock_create_cycle.call_count, 0)
        self.assertEqual(self.mock_is_active_cycle_exist.call_count, 1)


    @patch('cycle.repositories.cycle_repo.CycleRepo.get_active_cycle')
    def test_get_active_cycle(self, mock_get):
        mock_get.return_value = MagicMock()

        cycle = CycleService.get_active_cycle(self.supervisor)

        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(cycle, mock_get.return_value)
        mock_get.assert_called_with(self.supervisor)


    @patch('cycle.repositories.cycle_repo.CycleRepo.get_active_cycle')
    def test_get_active_cycle_not_exist(self, mock_get):
        mock_get.return_value = None

        with self.assertRaises(ValueError) as context:
            CycleService.get_active_cycle(self.supervisor)

        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(str(context.exception), "Siklus tidak ditemukan")
        mock_get.assert_called_with(self.supervisor)

    @patch('cycle.services.cycle_service.CycleService.get_stopped_cycle')
    def test_get_stopped_cycle(self, mock_get_stopped_cycle):
        mock_cycle = MagicMock(spec=Cycle)
        mock_get_stopped_cycle.return_value = [mock_cycle]

        cycles = CycleService.get_stopped_cycle(self.supervisor)

        self.assertEqual(mock_get_stopped_cycle.call_count, 1)
        self.assertEqual(cycles, [mock_cycle])
        mock_get_stopped_cycle.assert_called_with(self.supervisor)

    @patch('cycle.services.cycle_service.CycleService.get_stopped_cycle')
    def test_get_stopped_cycle_empty(self, mock_get_stopped_cycle):
        mock_get_stopped_cycle.return_value = []

        cycles = CycleService.get_stopped_cycle(self.supervisor)

        self.assertEqual(mock_get_stopped_cycle.call_count, 1)
        self.assertEqual(cycles, [])
        mock_get_stopped_cycle.assert_called_with(self.supervisor)

    def test_stop_cycle(self):
        mock_cycle = MagicMock(spec=Cycle)
        self.mock_get_cycle_by_id.return_value = mock_cycle

        stopped_cycle = CycleService.stop_cycle(str(mock_cycle.id), self.supervisor)

        self.assertEqual(self.mock_get_cycle_by_id.call_count, 1)
        self.assertEqual(self.mock_stop_cycle.call_count, 1)
        self.assertEqual(stopped_cycle, mock_cycle)
        self.mock_get_cycle_by_id.assert_called_with(str(mock_cycle.id))
        self.mock_stop_cycle.assert_called_with(str(mock_cycle.id))

    def test_stop_cycle_not_found(self):
        self.mock_get_cycle_by_id.return_value = None

        with self.assertRaises(ValueError) as context:
            CycleService.stop_cycle(str(uuid.uuid4()), self.supervisor)

        self.assertEqual(self.mock_get_cycle_by_id.call_count, 1)
        self.assertEqual(self.mock_stop_cycle.call_count, 0)
        self.assertEqual(str(context.exception), "Siklus tidak ditemukan")

    def test_get_stopped_cycle(self):
        stopped_cycle = Cycle.objects.create(
            start_date=date.today() - timedelta(days=30),
            end_date=date.today(),
            supervisor=self.user,
            is_stopped=True
        )

        other_cycle = Cycle.objects.create(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            supervisor=self.user,
            is_stopped=False
        )

        cycles = CycleService.get_stopped_cycle(self.user)

        self.assertEqual(len(cycles), 1)
        self.assertIn(stopped_cycle, cycles)
        self.assertNotIn(other_cycle, cycles)
