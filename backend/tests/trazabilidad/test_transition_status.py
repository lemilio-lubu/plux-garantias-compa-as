import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from application.dto.srg_body import TransitionSrgStatusDTO
from application.use_cases.srg.transition_status import TransitionSrgStatusUseCase
from domain.entities.srg import SrgEntity
from domain.exceptions.base import BusinessRuleViolationException, EntityNotFoundException
from domain.value_objects.srg_status import SrgStatus
from domain.value_objects.srg_type import SrgType


@pytest.fixture
def repo():
    return MagicMock()


def _srg(status=SrgStatus.PROCESO, srg_type=SrgType.WARRANTY):
    return SrgEntity(id=uuid4(), status=status, srg_type=srg_type, ot="202601739")


def test_proceso_to_pendiente(repo):
    srg = _srg()
    repo.find_by_id.return_value = srg
    repo.save.side_effect = lambda s: s

    dto = TransitionSrgStatusDTO(srg_id=srg.id, new_status="PENDIENTE")
    result = TransitionSrgStatusUseCase(repo).execute(dto)

    assert result.status == SrgStatus.PENDIENTE
    assert result.fecha_envio_marca is not None


def test_pendiente_to_preaprobado(repo):
    srg = _srg(status=SrgStatus.PENDIENTE)
    repo.find_by_id.return_value = srg
    repo.save.side_effect = lambda s: s

    dto = TransitionSrgStatusDTO(srg_id=srg.id, new_status="PREAPROBADO")
    result = TransitionSrgStatusUseCase(repo).execute(dto)
    assert result.status == SrgStatus.PREAPROBADO


def test_preaprobado_to_aprobado_with_fecha(repo):
    from datetime import date
    srg = _srg(status=SrgStatus.PREAPROBADO)
    repo.find_by_id.return_value = srg
    repo.save.side_effect = lambda s: s

    today = date.today().isoformat()
    dto = TransitionSrgStatusDTO(srg_id=srg.id, new_status="APROBADO", fecha_aprobacion=today)
    result = TransitionSrgStatusUseCase(repo).execute(dto)

    assert result.status == SrgStatus.APROBADO
    assert str(result.fecha_aprobacion) == today


def test_campaign_proceso_to_aprobado_direct(repo):
    """Campaign SRGs can be approved directly from PROCESO."""
    srg = _srg(srg_type=SrgType.CAMPAIGN)
    repo.find_by_id.return_value = srg
    repo.save.side_effect = lambda s: s

    dto = TransitionSrgStatusDTO(srg_id=srg.id, new_status="APROBADO")
    result = TransitionSrgStatusUseCase(repo).execute(dto)
    assert result.status == SrgStatus.APROBADO


def test_warranty_proceso_to_aprobado_raises(repo):
    """Warranties CANNOT go directly from PROCESO to APROBADO."""
    srg = _srg(srg_type=SrgType.WARRANTY)
    repo.find_by_id.return_value = srg

    dto = TransitionSrgStatusDTO(srg_id=srg.id, new_status="APROBADO")
    with pytest.raises(BusinessRuleViolationException):
        TransitionSrgStatusUseCase(repo).execute(dto)


def test_pendiente_to_negado(repo):
    srg = _srg(status=SrgStatus.PENDIENTE)
    repo.find_by_id.return_value = srg
    repo.save.side_effect = lambda s: s

    dto = TransitionSrgStatusDTO(srg_id=srg.id, new_status="NEGADO")
    result = TransitionSrgStatusUseCase(repo).execute(dto)
    assert result.status == SrgStatus.NEGADO


def test_srg_not_found_raises(repo):
    repo.find_by_id.return_value = None
    dto = TransitionSrgStatusDTO(srg_id=uuid4(), new_status="PENDIENTE")
    with pytest.raises(EntityNotFoundException):
        TransitionSrgStatusUseCase(repo).execute(dto)
