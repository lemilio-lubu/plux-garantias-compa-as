from application.dto.srg_body import RegisterPartMovementDTO
from application.ports.repositories.srg_body_repository import (
    ISrgEventRepository,
    ISrgPartRepository,
)
from domain.entities.srg_event import SrgEventEntity
from domain.exceptions.base import BusinessRuleViolationException, EntityNotFoundException
from domain.value_objects.srg_event import PartLedger, SrgEventType


class RegisterPartMovementUseCase:
    """Records a reception / work / return movement against a part, validating
    the quantity against the current ledger and appending an event."""

    def __init__(
        self,
        part_repo: ISrgPartRepository,
        event_repo: ISrgEventRepository,
    ) -> None:
        self._part_repo = part_repo
        self._event_repo = event_repo

    def execute(self, dto: RegisterPartMovementDTO) -> SrgEventEntity:
        part = self._part_repo.find_by_id(dto.part_id)
        if part is None:
            raise EntityNotFoundException("SrgPart", str(dto.part_id))

        if dto.quantity < 1:
            raise BusinessRuleViolationException("La cantidad debe ser mayor a cero.")

        try:
            event_type = SrgEventType(dto.event_type)
        except ValueError as exc:
            raise BusinessRuleViolationException(
                f"Tipo de movimiento inválido: {dto.event_type}"
            ) from exc

        counters = self._event_repo.part_counters(part.srg_id).get(part.id, {})
        ledger = PartLedger.from_counters(part.quantity, counters)

        self._validate(event_type, dto.quantity, ledger)

        event = SrgEventEntity(
            srg_id=part.srg_id,
            srg_part_id=part.id,
            actor_id=dto.actor_id,
            actor_role=dto.actor_role,
            event_type=event_type.value,
            quantity=dto.quantity,
            note=dto.note,
        )
        return self._event_repo.save(event)

    @staticmethod
    def _validate(event_type: SrgEventType, qty: int, ledger: PartLedger) -> None:
        if event_type == SrgEventType.RECEPTION_REGISTERED:
            if qty > ledger.pending_reception:
                raise BusinessRuleViolationException(
                    f"No se puede recibir más de lo solicitado. "
                    f"Pendiente: {ledger.pending_reception}."
                )
        elif event_type == SrgEventType.WORK_REGISTERED:
            available = ledger.received - ledger.used
            if qty > available:
                raise BusinessRuleViolationException(
                    f"No se puede instalar más de lo recibido. Disponible: {available}."
                )
        elif event_type == SrgEventType.CORE_RETURN_DECLARED:
            available = ledger.used - ledger.returned_declared
            if qty > available:
                raise BusinessRuleViolationException(
                    f"No se pueden devolver más cores de los instalados. "
                    f"Disponible: {available}."
                )
        elif event_type == SrgEventType.RETURN_CONFIRMED:
            available = ledger.returned_declared - ledger.returned_confirmed
            if qty > available:
                raise BusinessRuleViolationException(
                    f"No se puede confirmar más de lo declarado. Disponible: {available}."
                )
        else:
            raise BusinessRuleViolationException(
                f"El tipo {event_type} no es un movimiento de repuesto."
            )
