import pytest
from domain.value_objects.srg_status import SrgStatus
from domain.entities.srg import SrgEntity
from domain.exceptions.base import BusinessRuleViolationException


def test_valid_transition_proceso_to_pendiente():
    srg = SrgEntity(status=SrgStatus.PROCESO)
    srg.transition_to(SrgStatus.PENDIENTE)
    assert srg.status == SrgStatus.PENDIENTE
    assert srg.fecha_envio_marca is not None


def test_invalid_transition_raises():
    srg = SrgEntity(status=SrgStatus.PROCESO)
    with pytest.raises(BusinessRuleViolationException):
        srg.transition_to(SrgStatus.APROBADO)


def test_transition_aprobado_sets_fecha():
    from datetime import date
    srg = SrgEntity(status=SrgStatus.PREAPROBADO)
    today = date.today()
    srg.transition_to(SrgStatus.APROBADO, fecha_aprobacion=today)
    assert srg.status == SrgStatus.APROBADO
    assert srg.fecha_aprobacion == today
