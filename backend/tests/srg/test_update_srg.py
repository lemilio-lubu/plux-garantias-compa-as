import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from application.use_cases.srg.update_srg import UpdateSrgDTO, UpdateSrgUseCase
from application.use_cases.srg.get_dashboard import GetDashboardUseCase
from domain.entities.srg import SrgEntity
from domain.exceptions.base import BusinessRuleViolationException, EntityNotFoundException
from domain.value_objects.srg_status import SrgStatus
from domain.value_objects.srg_type import SrgType


@pytest.fixture
def repo():
    return MagicMock()


def _srg(status=SrgStatus.PROCESO):
    return SrgEntity(id=uuid4(), status=status, srg_type=SrgType.WARRANTY, ot="202601739",
                     vin="OLD_VIN", vehicle_model="OLD", concesionaria="SURMOTOR")


# ── UpdateSrg ──────────────────────────────────────────────────────────────

def test_update_srg_in_proceso(repo):
    srg = _srg(SrgStatus.PROCESO)
    repo.find_by_id.return_value = srg
    repo.save.side_effect = lambda s: s

    dto = UpdateSrgDTO(id=srg.id, vin="u5ypu81davl520154", vehicle_model="stonic")
    result = UpdateSrgUseCase(repo).execute(dto)

    assert result.vin == "U5YPU81DAVL520154"
    assert result.vehicle_model == "STONIC"


def test_update_srg_in_retornado(repo):
    srg = _srg(SrgStatus.RETORNADO)
    repo.find_by_id.return_value = srg
    repo.save.side_effect = lambda s: s

    dto = UpdateSrgDTO(id=srg.id, vehicle_color="rojo")
    result = UpdateSrgUseCase(repo).execute(dto)
    assert result.vehicle_color == "ROJO"


def test_update_srg_in_pendiente_raises(repo):
    srg = _srg(SrgStatus.PENDIENTE)
    repo.find_by_id.return_value = srg

    dto = UpdateSrgDTO(id=srg.id, vin="NEWVIN123456789AB")
    with pytest.raises(BusinessRuleViolationException) as exc:
        UpdateSrgUseCase(repo).execute(dto)
    assert "PENDIENTE" in exc.value.message


def test_update_srg_not_found_raises(repo):
    repo.find_by_id.return_value = None
    with pytest.raises(EntityNotFoundException):
        UpdateSrgUseCase(repo).execute(UpdateSrgDTO(id=uuid4()))


# ── Dashboard ──────────────────────────────────────────────────────────────

def test_dashboard_aggregates_correctly(repo):
    repo.get_dashboard_stats.return_value = [
        {"srg_type": "WARRANTY", "status": "PROCESO", "count": 3},
        {"srg_type": "WARRANTY", "status": "PENDIENTE", "count": 5},
        {"srg_type": "CAMPAIGN", "status": "APROBADO", "count": 2},
    ]
    result = GetDashboardUseCase(repo).execute("SURMOTOR")

    assert result.total == 10
    assert result.by_type == {"WARRANTY": 8, "CAMPAIGN": 2}

    status_map = {s.status: s.count for s in result.by_status}
    assert status_map["PROCESO"] == 3
    assert status_map["PENDIENTE"] == 5
    assert status_map["APROBADO"] == 2

    assert len(result.breakdown) == 3


def test_dashboard_empty_concesionaria(repo):
    repo.get_dashboard_stats.return_value = []
    result = GetDashboardUseCase(repo).execute("SHYRIS")

    assert result.total == 0
    assert result.by_type == {"WARRANTY": 0, "CAMPAIGN": 0}
    assert all(s.count == 0 for s in result.by_status)
