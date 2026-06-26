from dataclasses import dataclass
from enum import StrEnum


class SrgEventType(StrEnum):
    PART_REQUESTED = "PART_REQUESTED"
    RECEPTION_REGISTERED = "RECEPTION_REGISTERED"
    WORK_REGISTERED = "WORK_REGISTERED"
    CORE_RETURN_DECLARED = "CORE_RETURN_DECLARED"
    RETURN_CONFIRMED = "RETURN_CONFIRMED"
    STATUS_CHANGED = "STATUS_CHANGED"


class ReceptionState(StrEnum):
    PENDIENTE = "PENDIENTE"
    PARCIAL = "PARCIAL"
    COMPLETA = "COMPLETA"


class ReturnState(StrEnum):
    NO_APLICA = "NO_APLICA"
    PENDIENTE = "PENDIENTE"
    PARCIAL = "PARCIAL"
    COMPLETA = "COMPLETA"


# event_type -> ledger counter it feeds
COUNTER_OF: dict[str, str] = {
    SrgEventType.RECEPTION_REGISTERED.value: "received",
    SrgEventType.WORK_REGISTERED.value: "used",
    SrgEventType.CORE_RETURN_DECLARED.value: "returned_declared",
    SrgEventType.RETURN_CONFIRMED.value: "returned_confirmed",
}


@dataclass(frozen=True)
class PartLedger:
    """Derived view of a part's quantities, computed from the event ledger."""

    requested: int
    received: int = 0
    used: int = 0
    returned_declared: int = 0
    returned_confirmed: int = 0

    @classmethod
    def from_counters(cls, requested: int, counters: dict[str, int]) -> "PartLedger":
        return cls(
            requested=requested,
            received=counters.get("received", 0),
            used=counters.get("used", 0),
            returned_declared=counters.get("returned_declared", 0),
            returned_confirmed=counters.get("returned_confirmed", 0),
        )

    @property
    def pending_reception(self) -> int:
        return max(self.requested - self.received, 0)

    @property
    def pending_return(self) -> int:
        return max(self.used - self.returned_confirmed, 0)

    @property
    def reception_state(self) -> ReceptionState:
        if self.received <= 0:
            return ReceptionState.PENDIENTE
        if self.received < self.requested:
            return ReceptionState.PARCIAL
        return ReceptionState.COMPLETA

    @property
    def return_state(self) -> ReturnState:
        if self.used <= 0:
            return ReturnState.NO_APLICA
        if self.returned_confirmed <= 0:
            return ReturnState.PENDIENTE
        if self.returned_confirmed < self.used:
            return ReturnState.PARCIAL
        return ReturnState.COMPLETA

    @property
    def closed(self) -> bool:
        return self.reception_state == ReceptionState.COMPLETA and self.return_state in (
            ReturnState.COMPLETA,
            ReturnState.NO_APLICA,
        )
