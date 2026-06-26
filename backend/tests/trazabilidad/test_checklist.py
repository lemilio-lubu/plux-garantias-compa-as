import pytest
from unittest.mock import MagicMock
from decimal import Decimal
from uuid import uuid4

from application.dto.srg_body import AddSrgPartDTO, RegisterPartMovementDTO
from application.use_cases.srg.add_srg_part import AddSrgPartUseCase
from application.use_cases.srg.register_part_movement import RegisterPartMovementUseCase
from domain.entities.srg import SrgEntity
from domain.entities.srg_part import SrgPartEntity
from domain.exceptions.base import BusinessRuleViolationException
from domain.value_objects.srg_event import (
    PartLedger,
    ReceptionState,
    ReturnState,
    SrgEventType,
)
from domain.value_objects.srg_status import SrgStatus
from domain.value_objects.srg_type import SrgType


@pytest.fixture
def srg_repo():
    return MagicMock()


@pytest.fixture
def part_repo():
    return MagicMock()


@pytest.fixture
def event_repo():
    repo = MagicMock()
    repo.part_counters.return_value = {}
    repo.save.side_effect = lambda e: e
    return repo


# ── Add part ────────────────────────────────────────────────────────────────

def test_add_part_in_proceso_is_allowed_and_emits_event(srg_repo, part_repo, event_repo):
    srg = SrgEntity(id=uuid4(), status=SrgStatus.PROCESO, srg_type=SrgType.WARRANTY)
    srg_repo.find_by_id.return_value = srg
    saved = SrgPartEntity(id=uuid4(), srg_id=srg.id, catalog_code="SP-1001", quantity=3)
    part_repo.save.return_value = saved

    dto = AddSrgPartDTO(
        srg_id=srg.id, catalog_code="sp-1001", name_es="bomba de agua",
        quantity=3, unit_price=Decimal("84.50"), part_origin="kia", invoice_number="f-1",
    )
    AddSrgPartUseCase(srg_repo, part_repo, event_repo).execute(
        dto, actor_id=uuid4(), actor_role="ASESOR"
    )

    saved_arg = part_repo.save.call_args[0][0]
    assert saved_arg.catalog_code == "SP-1001"
    assert saved_arg.part_origin == "KIA"

    event = event_repo.save.call_args[0][0]
    assert event.event_type == SrgEventType.PART_REQUESTED.value
    assert event.quantity == 3


def test_add_part_to_campaign_raises(srg_repo, part_repo, event_repo):
    srg = SrgEntity(id=uuid4(), status=SrgStatus.PROCESO, srg_type=SrgType.CAMPAIGN)
    srg_repo.find_by_id.return_value = srg

    dto = AddSrgPartDTO(
        srg_id=srg.id, catalog_code="X", name_es="Y",
        quantity=1, unit_price=Decimal("1"), part_origin="KIA", invoice_number="F-1",
    )
    with pytest.raises(BusinessRuleViolationException):
        AddSrgPartUseCase(srg_repo, part_repo, event_repo).execute(dto)


# ── Reception ───────────────────────────────────────────────────────────────

def _part(quantity=5):
    return SrgPartEntity(id=uuid4(), srg_id=uuid4(), quantity=quantity)


def _movement(part, event_type, quantity):
    return RegisterPartMovementDTO(
        srg_id=part.srg_id, part_id=part.id, event_type=event_type,
        quantity=quantity, actor_id=uuid4(), actor_role="BODEGUERO",
    )


def test_reception_within_requested_ok(part_repo, event_repo):
    part = _part(5)
    part_repo.find_by_id.return_value = part

    dto = _movement(part, SrgEventType.RECEPTION_REGISTERED.value, 3)
    event = RegisterPartMovementUseCase(part_repo, event_repo).execute(dto)

    assert event.event_type == SrgEventType.RECEPTION_REGISTERED.value
    assert event.quantity == 3


def test_reception_exceeding_requested_raises(part_repo, event_repo):
    part = _part(5)
    part_repo.find_by_id.return_value = part
    event_repo.part_counters.return_value = {part.id: {"received": 4}}

    dto = _movement(part, SrgEventType.RECEPTION_REGISTERED.value, 3)
    with pytest.raises(BusinessRuleViolationException):
        RegisterPartMovementUseCase(part_repo, event_repo).execute(dto)


def test_work_cannot_exceed_received(part_repo, event_repo):
    part = _part(5)
    part_repo.find_by_id.return_value = part
    event_repo.part_counters.return_value = {part.id: {"received": 3, "used": 0}}

    dto = _movement(part, SrgEventType.WORK_REGISTERED.value, 4)
    with pytest.raises(BusinessRuleViolationException):
        RegisterPartMovementUseCase(part_repo, event_repo).execute(dto)


def test_core_return_declared_within_used_ok(part_repo, event_repo):
    part = _part(2)
    part_repo.find_by_id.return_value = part
    event_repo.part_counters.return_value = {part.id: {"received": 2, "used": 2}}

    dto = _movement(part, SrgEventType.CORE_RETURN_DECLARED.value, 2)
    event = RegisterPartMovementUseCase(part_repo, event_repo).execute(dto)
    assert event.quantity == 2


def test_return_confirmed_cannot_exceed_declared(part_repo, event_repo):
    part = _part(2)
    part_repo.find_by_id.return_value = part
    event_repo.part_counters.return_value = {
        part.id: {"received": 2, "used": 2, "returned_declared": 1, "returned_confirmed": 0}
    }

    dto = _movement(part, SrgEventType.RETURN_CONFIRMED.value, 2)
    with pytest.raises(BusinessRuleViolationException):
        RegisterPartMovementUseCase(part_repo, event_repo).execute(dto)


# ── Ledger states ───────────────────────────────────────────────────────────

def test_part_ledger_partial_reception():
    ledger = PartLedger.from_counters(5, {"received": 3})
    assert ledger.reception_state == ReceptionState.PARCIAL
    assert ledger.pending_reception == 2


def test_part_ledger_fully_closed():
    ledger = PartLedger.from_counters(
        5, {"received": 5, "used": 5, "returned_declared": 5, "returned_confirmed": 5}
    )
    assert ledger.reception_state == ReceptionState.COMPLETA
    assert ledger.return_state == ReturnState.COMPLETA
    assert ledger.closed
